# -*- coding: utf-8 -*-
from datetime import datetime as dt
from django.conf import settings
from django.contrib.sites.models import Site
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template import Context, Template
from django.template.loader import get_template
from django.http import Http404
from models import Zone, Banner
import random


def banner(request, banner_id):
    b = get_object_or_404(Banner, id=banner_id)
    b.clicks = b.clicks + 1
    b.save()
    return HttpResponseRedirect(b.foreign_url)
def zonesjs(request):
    template = get_template("zones.js")
    zones = Zone.objects.all()
    output_list = []
    for row in zones:
	output_list.append( { row.id: gen_banner_code(request, row.id) } )
    context = Context({
	"zones":zones,
	"banners":output_list
	})
    return HttpResponse(template.render(context),content_type="text/javascript")
def zonejs(request,zonejs_id):
    template = get_template("banners.js")
    zone = get_object_or_404(Zone,id=zonejs_id)
    context = Context({
	"banner_code":gen_banner_code(request, zonejs_id),
	"MEDIA_URL":settings.MEDIA_URL,
	"html_after_banner":zone.html_after_banner,
	"html_pre_banner":zone.html_pre_banner,
	"zone_id":zonejs_id
	})
    return HttpResponse(template.render(context),content_type="text/javascript")

def zones(request, zone_id):
    template = get_template("iBanners/zones.html")
    zone = Zone.objects.get(id=zone_id)
    context = Context({
        "banner_code":gen_banner_code(request, zone_id),
        "MEDIA_URL":settings.MEDIA_URL,
        "html_after_banner":zone.html_after_banner,
        "html_pre_banner":zone.html_pre_banner
    })
    return HttpResponse(template.render(context))

# Функиция, возвращающая HTML код для ibanners
def gen_banner_code(request, zone_id, var=False):
    pr = {1:3, 2:5, 3:7, 4:9, 5:11, 6:13, 7:15, 8:17, 9:20} # Распределение вероятностей
    probabilities = []

    site = Site.objects.get_current()
    banner_site_url = getattr(settings, 'BANNER_SITE_URL', 'http://%s/' % site.domain)

    if not request.META.has_key('ibanners.clients'): request.META['ibanners.clients'] = []

    # Поиск зоны
    try: zone = Zone.objects.get(id=zone_id)
    except: zone = None

    # Поиск по переменным
    if not var:
        var = request.GET.get('var', False)
    varnot = request.GET.get('varnot', False)

    if zone:
        banners = Banner.objects.filter(
            (Q(campaign__begin_date__lte=dt.now()) | Q(campaign__begin_date__isnull=True)),
            (Q(campaign__end_date__gte=dt.now()) | Q(campaign__end_date__isnull=True)),
            (Q(begin_date__lte=dt.now()) | Q(begin_date__isnull=True)),
            (Q(end_date__gte=dt.now()) | Q(end_date__isnull=True)),
            zones=zone).exclude(campaign__client__in=request.META['ibanners.clients']).order_by('-campaign__priority')
        if var: banners = banners.filter(var=var)
        if varnot: banners = banners.exclude(var=varnot)
        count = banners.count()

        banner = False
        hbanner = u""
        if count == 1:
            banner = banners[0]
        elif count > 1:
            # Поиск самого крутого баннера в зоне, в зависимости от самой крутой кампании
            for b in banners:
                if ((b.shows < b.max_shows) or (b.max_shows == 0)) and ((b.clicks < b.max_clicks) or (b.max_clicks == 0)):
                    if int(b.campaign.priority) == 10:
                        banner = b
                        break
            # Если крутой баннер не найден, то ищем простые баннеры, исключая собственные кампании
            if not banner:
                banners2 = banners.exclude(campaign__priority=0)
                # Если такие банеры есть строим полосу вероятностей
                if banners2.count() > 0:
                    for b in banners2:
                        if ((b.shows < b.max_shows) or (b.max_shows == 0)) and ((b.clicks < b.max_clicks) or (b.max_clicks == 0)):
                            for unused in range(pr[b.campaign.priority]):
                                probabilities.append(b.campaign.priority)
                    priority = random.choice(probabilities)
                    banners2 = Banner.objects.filter(
                        (Q(campaign__begin_date__lte=dt.now()) | Q(campaign__begin_date__isnull=True)),
                        (Q(campaign__end_date__gte=dt.now()) | Q(campaign__end_date__isnull=True)),
                        (Q(begin_date__lte=dt.now()) | Q(begin_date__isnull=True)),
                        (Q(end_date__gte=dt.now()) | Q(end_date__isnull=True)),
                        zones=zone, campaign__priority=priority).exclude(campaign__client__in=request.META['ibanners.clients']).order_by('-campaign__priority')
                    # Если в вероятность попал один баннер
                    if banners2.count() == 1:
                        banner = banners2[0]
                    # Если в вероятность попало более одного баннера, то выбираем из равновероятного
                    elif banners2.count() > 1:
                        bids = []
                        for b in banners2:
                            if ((b.shows < b.max_shows) or (b.max_shows == 0)) and ((b.clicks < b.max_clicks) or (b.max_clicks == 0)):
                                bids.append(b.id)
                        bid = random.choice(bids)
                        banner = banners2.get(id=bid)
                    else:
                        pass
            # На данном этапе остались только собственные кампании
            if not banner:
                bids = []
                for b in banners:
                    if ((b.shows < b.max_shows) or (b.max_shows == 0)) and ((b.clicks < b.max_clicks) or (b.max_clicks == 0)):
                        bids.append(b.id)
                bid = random.choice(bids)
                banner = banners.get(id=bid)

        # Если баннер всё-таки найден
        if banner:
            # Добавляем клиента, чтобы потом не показывать его баннер
            if not request.META['ibanners.clients'].__contains__(banner.campaign.client.id):
                if banner.campaign.client.one_banner_per_page:
                    request.META['ibanners.clients'].append(banner.campaign.client.id)
            banner.shows = banner.shows + 1
            banner.save()

            # Определяем пути до файла
            swf_file = str(banner.swf_file)
            img_file = str(banner.img_file)
            swf_banner_name = swf_file[swf_file.rfind('/') + 1:]
            img_banner_name = img_file[img_file.rfind('/') + 1:]
            swf_url = ""
            img_url = ""
            # Флэш баннер
            if banner.banner_type == 'f':
                try: swf_url = u"%sibas/swf/%s" % (settings.MEDIA_URL, swf_banner_name)
                except: swf_url
                try: img_url = u"%sibas/img/%s" % (settings.MEDIA_URL, img_banner_name)
                except: img_url = ""
            # Графический баннер
            if banner.banner_type == 'g':
                try: img_url = u"%sibas/img/%s" % (settings.MEDIA_URL, img_banner_name)
                except: img_url = ""
	    # Тизерный баннер
	    if banner.banner_type == 't':
                try: swf_url = u"%sibas/swf/%s" % (settings.MEDIA_URL, swf_banner_name)
                except: swf_url
                try: img_url = u"%sibas/img/%s" % (settings.MEDIA_URL, img_banner_name)
                except: img_url = ""
            code = u""
	    # JavaScript banners
	    if banner.banner_type == 'j':
		template = get_template("iBanners/gen_js_code.html")
		context = Context({
		    "alt":banner.alt,
		    "html_text":banner.html_text,
		    "zone_id":zone_id,
		})
		code += template.render(context)
            # flash баннеры
            if banner.banner_type == 'f':
                banner_href = u"%sibas/%s/" % (banner_site_url, banner.id)
                template = get_template("iBanners/gen_banner_code.html")
                context = Context({
                    "banner_width":banner.width,
                    "banner_height":banner.height,
                    "data":u"%s?link1=%s" % (swf_url, banner_href),
                    "swf_url":swf_url,
                    "banner_href":banner_href,
                    "img_url":img_url,
                    "foreign_url":banner.foreign_url,
                })
                code += template.render(context)
	    elif banner.banner_type == 't':
		banner_href = u"%sibas/%s/" % (banner_site_url, banner.id)
                template = get_template("iBanners/gen_tizer_code.html")
                context = Context({
                    "banner_width":banner.width,
                    "banner_height":banner.height,
                    "data":u"%s?link1=%s" % (swf_url, banner_href),
                    "swf_url":swf_url,
                    "banner_href":banner_href,
                    "img_url":img_url,
                    "foreign_url":banner.foreign_url,
		    "alt":banner.alt,
		    "comment":banner.comment,
		    "html_text":banner.html_text,
                })
                code += template.render(context)
            # графические баннеры
            elif banner.banner_type == 'g':
                if banner.foreign_url:
                    code += u"""<a href="%sibas/%s/">""" % (banner_site_url, banner.id)
                if banner.width:
                    bwidth = """width="%s" """ % banner.width
                else:
                    try:
                        bwidth = """width="%s" """ % banner.img_file.width
                    except:
                        bwidth = ''
                if banner.height:
                    bheight = """height="%s" """ % banner.height
                else:
                    try:
                        bheight = """height="%s" """ % banner.img_file.height
                    except:
                        bheight = ''
                code += u"""<img src="%s" alt="%s" %s%s/>""" % (img_url, banner.alt, bwidth, bheight)
                if banner.foreign_url:
                    code += u"""</a>"""
            # html баннеры
            elif banner.banner_type == 'h':
                if banner.allow_template_tags:
                    t = Template(banner.html_text)
                    code += t.render(Context({}))
                else:
                    code += banner.html_text
            hbanner = code
        else:
            pass
        if hbanner:
            return u"%s%s%s" % (zone.html_pre_banner, hbanner, zone.html_after_banner)
        else:
            return u""
    # Если зона не найдена
    else:
        return u""
