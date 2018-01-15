# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.views.generic import list_detail, simple
from django.contrib.sitemaps import Sitemap

from news.conf import settings as conf
from news.models import NewsArticle

##########################################################################
##########################################################################

#Для карты сайта
class NewsSitemap(Sitemap):
	changefreq = "monthly"
	priority = 0.5

	def items(self):
		return NewsArticle.objects.filter(is_active=True)

	def location(self, obj):
		return obj.get_item_url()

##########################################################################
##########################################################################

def all(request, template_name='news/news.html', extra_context=None):
	page = 1
	if 'page' in request.GET:
		try: page = int(request.GET.get('page'))
		except TypeError: raise Http404()

	objs = NewsArticle.objects.filter(is_active=True)

	return list_detail.object_list(
		request,
		queryset = objs,
		paginate_by = conf.PAGINATE_BY,
		page = page,
		template_name = template_name,
		template_object_name = 'news',
		extra_context = extra_context,
	)

##########################################################################
##########################################################################

def full(request, slug, template_name='news/item.html', extra_context=None):
	#try:
	#	id = int(id)
	#except TypeError:
#		raise Http404()

	objs = NewsArticle.objects.filter(is_active=True)

	return list_detail.object_detail(
		request,
		queryset = objs,
		slug = slug,
		template_name = template_name,
		extra_context = extra_context,
		template_object_name='item',
	)

##########################################################################
##########################################################################