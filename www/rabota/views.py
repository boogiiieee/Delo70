# -*- coding: utf-8 -*-

from django.template import loader, RequestContext
from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.views.generic.list_detail import object_list
from django.views.decorators.cache import cache_page
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.conf import settings
from django.db.models import Q
import datetime

from annoying.decorators import render_to
from annoying.utils import HttpResponseReload
from annoying.functions import get_object_or_None

from registration.backends.simple.views import RegistrationView

from geo.models import CustomLocation
from feedback.views import feedback_views

from rabota.models import Schedule, TypeEmployment, TypeWages, Education, Experience, Category, Vacancy, Resume, SubscribeVacancy, SubscribeResume
from rabota.forms import SearchMinForm, SearchVacancyForm, SearchResumeForm, AddVacancyForm, AddResumeForm, ProfileForm, RegistrationCaptchaForm,\
							AddVacancySubscribeForm, AddResumeSubscribeForm, TYPE_SEARCH
							
MAX_VIEWS_COUNT = 1000000

##########################################################################
##########################################################################

def count_col(c):
	if c>settings.PAGINATE_BY: 
		count = settings.PAGINATE_BY/2
		if not settings.PAGINATE_BY%2==0:
			count = count+1
	else: 
		if c%2==0:
			count = c/2
		else:
			count = c/2+1
	return count

def rublic_l():
	rubrics = Category.activs.all()
	count = rubrics.count()
	
	if count % 4 > 0:
		c = count / 4 + 1
	else:
		c = count / 4
	rubric_list = [ rubrics[0:c], rubrics[c:2*c], rubrics[2*c:3*c], rubrics[3*c:] ]
	
	return rubric_list
		
	
##########################################################################
##########################################################################

@render_to('index.html')
def index(request):
	rubric_list = rublic_l()
	
	vacancy_list = Vacancy.activs.filter(city=request.location)[:20]
			
	return {
		'last_vacancy': vacancy_list,
		'rubric_list': rubric_list,
		'active': 1,
	}

def contacts(request):
	return feedback_views(request, 'contacts.html')
	
##########################################################################
##########################################################################

##########################################################################
##########################################################################

#Вакансии
def vacancy(request, slug_city):
	try: page = int(request.GET.get('page', 1))
	except: page = 1
	
	items = Vacancy.activs.filter(city__slug=slug_city)[:2000]
	count = count_col( items.count() )
	
	try:city = CustomLocation.objects.get(slug=slug_city)
	except: raise Http404()
	
	rubric_list = rublic_l()
	
	return object_list(request,
		queryset = items,
		paginate_by = settings.PAGINATE_BY,
		page = page,
		template_name = 'rabota/vacancy.html',
		template_object_name = 'items',
		extra_context = {
			'count_col' : count,
			'active': 2,
			'rubric_list': rubric_list,
			'slug_city': slug_city,
			'city' : city
		},
	)
	
##########################################################################
##########################################################################

#Резюме
def resume(request, slug_city):
	try: page = int(request.GET.get('page', 1))
	except: page = 1
	
	items = Resume.activs.filter(city__slug=slug_city)[:2000]
	count = count_col(items.count())
	
	rubric_list = rublic_l()
	
	try:city = CustomLocation.objects.get(slug=slug_city)
	except: raise Http404()
	
	return object_list(request,
		queryset = items,
		paginate_by = settings.PAGINATE_BY,
		page = page,
		template_name = 'rabota/resume.html',
		template_object_name = 'items',
		extra_context = {
			'count_col' : count,
			'active':3,
			'search': SearchMinForm(type_search=TYPE_SEARCH[1][0]),
			'rubric_list': rubric_list,
			'slug_city': slug_city,
			'city' : city
		},
	)
	
##########################################################################
##########################################################################

##########################################################################
##########################################################################

#Вакансии по катерогиям
def category_vacancy(request, slug_city, id, slug):
	try: page = int(request.GET.get('page', 1))
	except: page = 1
	
	try:
		ct = Category.activs.get(id=id)
	except: raise Http404()
	
	items = Vacancy.activs.filter(category=ct, city__slug=slug_city)[:2000]
	count = count_col(items.count())
	
	rubric_list = rublic_l()

	try:city = CustomLocation.objects.get(slug=slug_city)
	except: raise Http404()
	
	return object_list(request,
		queryset = items,
		paginate_by = settings.PAGINATE_BY,
		page = page,
		template_name = 'rabota/vacancy_category.html',
		template_object_name = 'items',
		extra_context = {
			'count_col': count,
			'active': 2,
			'ct': ct,
			'rubric_list': rubric_list,
			'slug_city': slug_city,
			'city': city,
		},
	)
	
##########################################################################
##########################################################################

#Резюме по катерогиям
def category_resume(request, slug_city, id, slug):
	try: page = int(request.GET.get('page', 1))
	except: page = 1
	
	try:
		ct = Category.activs.get(id=id)
	except: raise Http404()
	
	items = Resume.activs.filter(category=ct, city__slug=slug_city)[:2000]
	count = count_col(items.count())
	
	rubric_list = rublic_l()
	
	try:city = CustomLocation.objects.get(slug=slug_city)
	except: raise Http404()
	
	return object_list(request,
		queryset = items,
		paginate_by = settings.PAGINATE_BY,
		page = page,
		template_name = 'rabota/resume_category.html',
		template_object_name = 'items',
		extra_context = {
			'count_col': count,
			'active': 3,
			'search': SearchMinForm(type_search=TYPE_SEARCH[1][0]),
			'ct': ct,
			'rubric_list': rubric_list,
			'slug_city': slug_city,
			'city': city,
		},
	)
	
##########################################################################
##########################################################################

##########################################################################
##########################################################################

@render_to('rabota/vacancy_item.html')
def vacancy_item(request, slug_city, id, ct=None, slug=None):
	if ct:
		try:
			ct = Category.activs.get(id=ct)
		except: raise Http404()
		try:
			item = Vacancy.objects.get(id=id, category=ct, city__slug=slug_city)
		except: raise Http404()
	else:
		try:
			item = Vacancy.objects.get(id=id, city__slug=slug_city)
		except Vacancy.DoesNotExist:
			return render(request, '404.html', {}, status=404)
		
	if item.is_active == False or item.in_archive == True:
		return render(request, '410.html', {}, status=410)
		
	if item.views_count < MAX_VIEWS_COUNT:
		item.views_count = item.views_count + 1
		item.save()
		
	try:city = CustomLocation.objects.get(slug=slug_city)
	except: raise Http404()
		
	return {
		'item': item,
		'active': 2,
		'ct': ct,
		'city': city,
	}

##########################################################################
##########################################################################

@render_to('rabota/resume_item.html')
def resume_item(request, slug_city, id, ct=None, slug=None):
	if ct:
		try:
			ct = Category.activs.get(id=ct)
		except: raise Http404()
		try:
			item = Resume.objects.get(id=id, category=ct, city__slug=slug_city)
		except: raise Http404()
	else:
		try:
			item = Resume.objects.get(id=id, city__slug=slug_city)
		except Resume.DoesNotExist:
			return render(request, '404.html', {}, status=404)
			
	if item.is_active == False or item.in_archive == True:
		return render(request, '410.html', {}, status=410)
		
	if item.views_count < MAX_VIEWS_COUNT:
		item.views_count = item.views_count + 1
		item.save()
		
	try:city = CustomLocation.objects.get(slug=slug_city)
	except: raise Http404()
		
	return {
		'item': item,
		'active': 3,
		'search': SearchMinForm(type_search=TYPE_SEARCH[1][0]),
		'ct': ct,
		'city': city,
	}

##########################################################################
##########################################################################

##########################################################################
##########################################################################

#Поиск вакансии
def vacancy_search(request, slug_city):
	try: page = int(request.GET.get('page', 1))
	except: page = 1
	
	query = Q(city__slug=slug_city)
	
	q = request.GET.get('q', False)
	
	if q: query = query & ( Q(post__icontains=q) | Q(brief__icontains=q) )
	if request.GET.getlist('category', False): query = query & Q(category__id__in=request.GET.getlist('category'))
		
	items = Vacancy.activs.filter(query).distinct()[:2000]
	count = count_col(items.count())
	
	category = []

	form = SearchMinForm()
	for key in request.GET:
		try:
			if key in ['category',]:
				form.fields[key].initial = request.GET.getlist(key)
				category = request.GET.getlist(key)
			else:
				form.fields[key].initial = request.GET.get(key)
		except KeyError:
			pass
	category = Category.activs.filter(pk__in=category)
	
	rubric_list = rublic_l()
	
	return object_list(request,
		queryset = items,
		paginate_by = settings.PAGINATE_BY,
		page = page,
		template_name = 'rabota/vacancy_search.html',
		template_object_name = 'items',
		extra_context = {
			'search': form,
			'count_col': count,
			'q': q,
			'category': category,
			'active': 2,
			'rubric_list': rubric_list,
		},
	)

##########################################################################
##########################################################################

#Поиск резюме
def resume_search(request, slug_city):
	try: page = int(request.GET.get('page', 1))
	except: page = 1
	
	query = Q(city__slug=slug_city)
	
	q = request.GET.get('q', False)
	
	if q: query = query & Q(post__icontains=q)
	if request.GET.getlist('category', False): query = query & Q(category__id__in=request.GET.getlist('category'))
		
	items = Resume.activs.filter(query).distinct()[:2000]
	count = count_col(items.count())

	category = []
	
	form = SearchMinForm(initial={'type_search': TYPE_SEARCH[1][0]})
	for key in request.GET:
		try:
			if key in ['category',]:
				form.fields[key].initial = request.GET.getlist(key)
				category = request.GET.getlist(key)
			else:
				form.fields[key].initial = request.GET.get(key)
		except KeyError:
			pass

	category = Category.activs.filter(pk__in=category)
	
	return object_list(request,
		queryset = items,
		paginate_by = settings.PAGINATE_BY,
		page = page,
		template_name = 'rabota/resume_search.html',
		template_object_name = 'items',
		extra_context = {
			'search': form,
			'count_col': count,
			'q': q,
			'category': category,
			'active': 3,
		},
	)

##########################################################################
##########################################################################

##########################################################################
##########################################################################

#Расширенный поиск вакансии
def vacancy_search_advanced(request, slug_city):
	try: page = int(request.GET.get('page', 1))
	except: page = 1
	
	try:
		city = CustomLocation.objects.get(slug=slug_city)
	except:
		raise Http404()
	
	query = Q()
	
	if request.GET.get('q', False): query = query & ( Q(post__icontains=request.GET.get('q')) | Q(brief__icontains=request.GET.get('q')) )
	if request.GET.getlist('category', False): query = query & Q(category__id__in=request.GET.getlist('category'))
	if request.GET.get('schedule', False): query = query & Q(schedule=request.GET.get('schedule'))
	if request.GET.get('type_employment', False): query = query & Q(type_employment=request.GET.get('type_employment'))
	if request.GET.get('wage_min', False): query = query & Q(wage_min__gte=request.GET.get('wage_min'))
	if request.GET.get('wage_max', False): query = query & Q(wage_max__lte=request.GET.get('wage_max'))
	if request.GET.get('type_wages', False): query = query & Q(type_wages=request.GET.get('type_wages'))
	if request.GET.get('education', False): query = query & Q(education=request.GET.get('education'))
	if request.GET.get('experience', False): query = query & Q(experience=request.GET.get('experience'))
	if request.GET.get('city', False):
		query = query & Q(city=request.GET.get('city'))
	else:
		query = query & Q(city=city)
		
	items = Vacancy.activs.filter(query).distinct()[:2000]
	count = count_col(items.count())
	
	form = SearchVacancyForm()
	form.fields['city'].initial = city
	for key in request.GET:
		try:
			if key in ['category',]:
				form.fields[key].initial = request.GET.getlist(key)
			else:
				form.fields[key].initial = request.GET.get(key)
		except KeyError:
			pass
	
	return object_list(request,
		queryset = items,
		paginate_by = settings.PAGINATE_BY,
		page = page,
		template_name = 'rabota/vacancy_search_advanced.html',
		template_object_name = 'items',
		extra_context = {
			'form': form,
			'count_col': count,
			'active': 2,
		},
	)
	
##########################################################################
##########################################################################

#Расширенный поиск резюме
def resume_search_advanced(request, slug_city):
	try: page = int(request.GET.get('page', 1))
	except: page = 1
	
	try:
		city = CustomLocation.objects.get(slug=slug_city)
	except:
		raise Http404()
	
	query = Q()
	
	if request.GET.get('q', False): query = query & Q(post__icontains=request.GET.get('q'))
	if request.GET.getlist('category', False): query = query & Q(category__id__in=request.GET.getlist('category'))
	if request.GET.get('schedule', False): query = query & Q(schedule=request.GET.get('schedule'))
	if request.GET.get('type_employment', False): query = query & Q(type_employment=request.GET.get('type_employment'))
	if request.GET.get('wage_min', False): query = query & Q(wage_min__gte=request.GET.get('wage_min'))
	if request.GET.get('type_wages', False): query = query & Q(type_wages=request.GET.get('type_wages'))
	if request.GET.get('experience', False): query = query & Q(experience=request.GET.get('experience'))
	if request.GET.get('education', False): query = query & Q(education=request.GET.get('education'))
	if request.GET.get('city', False):
		query = query & Q(city=request.GET.get('city'))
	else:
		query = query & Q(city=city)
		
	items = Resume.activs.filter(query).distinct()[:2000]
	count = count_col(items.count())
	
	form = SearchResumeForm()
	form.fields['city'].initial = city
	for key in request.GET:
		try:
			if key in ['category',]:
				form.fields[key].initial = request.GET.getlist(key)
			else:
				form.fields[key].initial = request.GET.get(key)
		except KeyError:
			pass
	
	return object_list(request,
		queryset = items,
		paginate_by = settings.PAGINATE_BY,
		page = page,
		template_name = 'rabota/resume_search_advanced.html',
		template_object_name = 'items',
		extra_context = {
			'form': form,
			'count_col': count,
			'active': 3,
			'search': SearchMinForm(type_search=TYPE_SEARCH[1][0]),
		},
	)

##########################################################################
##########################################################################

##########################################################################
##########################################################################

@render_to('rabota/vacancy_add.html')
def vacancy_add(request, slug_city):
	if request.method != 'POST' and not request.user.is_authenticated():
		messages.add_message(request, messages.WARNING, u'Внимание! Вы не зарегистрированы. Незарегистрированые пользователи не могут редактировать и удалять свои вакансии.')
		
	try:
		city = CustomLocation.objects.get(slug=slug_city)
	except:
		raise Http404()
		
	obj = Vacancy(user=request.user if request.user.is_authenticated() else None, stick_date=datetime.datetime.now()+datetime.timedelta(days=7), city=city)
	form = AddVacancyForm(request.POST or None, request.FILES or None, instance=obj)
	if form.is_valid():
		form.save()
		messages.add_message(request, messages.SUCCESS, u'Вакансия успешно добавлена и появится на сайте в течение трех часов.')
		
		if request.user.is_authenticated():
			return HttpResponseRedirect(
				reverse('account_vacancy', args=[], kwargs={'username':request.user.username})
			)
		return HttpResponseRedirect(
			reverse('vacancy', args=[], kwargs={'slug_city':request.location.slug,})
		)
		
	return {
		'form': form,
		'active': 2,
	}
	
##########################################################################
##########################################################################

@render_to('rabota/resume_add.html')
def resume_add(request, slug_city):
	if request.method != 'POST' and not request.user.is_authenticated():
		messages.add_message(request, messages.WARNING, u'Внимание! Вы не зарегистрированы. Незарегистрированые пользователи не могут редактировать и удалять свои резюме.')
		
	try:
		city = CustomLocation.objects.get(slug=slug_city)
	except:
		raise Http404()
		
	obj = Resume(user=request.user if request.user.is_authenticated() else None, city=city)
	form = AddResumeForm(request.POST or None, request.FILES or None, instance=obj)
	if form.is_valid():
		form.save()
		messages.add_message(request, messages.SUCCESS, u'Резюме успешно добавлено и появится на сайте в течение трех часов.')
		
		if request.user.is_authenticated():
			return HttpResponseRedirect(
				reverse('account_resume', args=[], kwargs={'username':request.user.username})
			)
		return HttpResponseRedirect(
			reverse('resume', args=[], kwargs={'slug_city':request.location.slug,})
		)
		
	return {
		'form': form,
		'active': 3,
		'search': SearchMinForm(type_search=TYPE_SEARCH[1][0]),
	}
	
##########################################################################
##########################################################################

##########################################################################
##########################################################################

@login_required
@render_to('rabota/vacancy_subscribe_add.html')
def vacancy_subscribe_add(request):
	obj = SubscribeVacancy(user=request.user, city=request.location)
	form = AddVacancySubscribeForm(request.POST or None, instance=obj)
	if form.is_valid():
		if SubscribeVacancy.objects.filter(user=request.user).count():
			messages.add_message(request, messages.WARNING, u'Вы можете добавить не более одной подписки на вакансии.')
			return HttpResponseReload(request)
		else:
			if not request.user.email:
				messages.add_message(request, messages.WARNING, u'Чтобы получать уведомления вам необходимо заполнить поле "e-mail" в разделе "Профиль".')
				
			form.save()
			messages.add_message(request, messages.SUCCESS, u'Подписка на вакансии успешно добавлена на 30 дней.')
			
			return HttpResponseRedirect(
				reverse('account_subscribe', args=[], kwargs={'username':request.user.username})
			)
		
	return {
		'form': form,
		'account_active': 4,
	}
	
##########################################################################
##########################################################################

@login_required
@render_to('rabota/resume_subscribe_add.html')
def resume_subscribe_add(request):
	obj = SubscribeResume(user=request.user, city=request.location)
	form = AddResumeSubscribeForm(request.POST or None, instance=obj)
	if form.is_valid():
		if SubscribeResume.objects.filter(user=request.user).count():
			messages.add_message(request, messages.WARNING, u'Вы можете добавить не более одной подписки на вакансии.')
		else:
			if not request.user.email:
				messages.add_message(request, messages.WARNING, u'Чтобы получать уведомления вам необходимо заполнить поле "e-mail" в личном кабинете.')
				
			form.save()
			messages.add_message(request, messages.SUCCESS, u'Подписка на резюме успешно добавлена на 30 дней.')
		return HttpResponseRedirect(
			reverse('account_subscribe', args=[], kwargs={'username':request.user.username})
		)
		
	return {
		'form': form,
		'account_active': 4,
		'search': SearchMinForm(type_search=TYPE_SEARCH[1][0]),
	}
	
##########################################################################
##########################################################################

##########################################################################
##########################################################################

@login_required
def vacancy_subscribe_del(request):
	try:
		SubscribeVacancy.activs.filter(user=request.user).delete()
	except:
		messages.add_message(request, messages.ERROR, 'Ошибка удаления подписки! Обратитесь к администратору.')
	else:
		messages.add_message(request, messages.INFO, 'Подписка успешно удалена. Вы больше не будете получать уведомления о новых вакансиях.')
		
	return HttpResponseRedirect(
		reverse('account_subscribe', args=[], kwargs={'username':request.user.username})
	)
	
##########################################################################
##########################################################################

@login_required
def resume_subscribe_del(request):
	try:
		SubscribeResume.activs.filter(user=request.user).delete()
	except:
		messages.add_message(request, messages.ERROR, 'Ошибка удаления подписки! Обратитесь к администратору.')
	else:
		messages.add_message(request, messages.INFO, 'Подписка успешно удалена. Вы больше не будете получать уведомления о новых резюме.')
		
	return HttpResponseRedirect(
		reverse('account_subscribe', args=[], kwargs={'username':request.user.username})
	)

##########################################################################
##########################################################################

##########################################################################
##########################################################################

@login_required
def account_vacancy(request, username):
	try: page = int(request.GET.get('page', 1))
	except: page = 1

	items = Vacancy.objects.filter(is_active=True, user=request.user)

	return object_list(request,
		queryset = items,
		paginate_by = settings.PAGINATE_BY,
		page = page,
		template_name = 'rabota/account_vacancy.html',
		template_object_name = 'items',
		extra_context = {'account_active':2,},
	)
	
##########################################################################
##########################################################################

@login_required
def account_resume(request, username):
	try: page = int(request.GET.get('page', 1))
	except: page = 1

	items = Resume.objects.filter(is_active=True, user=request.user)

	return object_list(request,
		queryset = items,
		paginate_by = settings.PAGINATE_BY,
		page = page,
		template_name = 'rabota/account_resume.html',
		template_object_name = 'items',
		extra_context = {'account_active':3, 'search': SearchMinForm(type_search=TYPE_SEARCH[1][0]),},
	)

##########################################################################
##########################################################################

##########################################################################
##########################################################################

@login_required
@render_to('rabota/account_vacancy_item.html')
def account_vacancy_item(request, username, id):
	try:
		obj = Vacancy.activs.get(user=request.user, id=id)
	except:
		raise Http404()
		
	form = AddVacancyForm(request.POST or None, request.FILES or None, instance=obj)
	if form.is_valid():
		form.save()
		messages.add_message(request, messages.SUCCESS, u'Вакансия успешно сохранена. Изменения появятся на сайте в течение трех часов.')
		return HttpResponseReload(request)
		
	return {
		'form': form,
		'account_active': 2,
	}

##########################################################################
##########################################################################

@login_required
@render_to('rabota/account_resume_item.html')
def account_resume_item(request, username, id):
	try:
		obj = Resume.activs.get(user=request.user, id=id)
	except:
		raise Http404()
		
	form = AddResumeForm(request.POST or None, request.FILES or None, instance=obj)
	if form.is_valid():
		form.save()
		messages.add_message(request, messages.SUCCESS, u'Резюме успешно сохранено. Изменения появятся на сайте в течение трех часов.')
		return HttpResponseReload(request)
		
	return {
		'form': form,
		'account_active': 3,
		'search': SearchMinForm(type_search=TYPE_SEARCH[1][0]),
	}

##########################################################################
##########################################################################

##########################################################################
##########################################################################
	
@login_required
def vacancy_del(request, username, id):
	try:
		obj = Vacancy.activs.get(user=request.user, id=id)
	except:
		messages.add_message(request, messages.ERROR, 'Ошибка перемещения вакансии в архив! Обратитесь к администратору.')
	else:
		obj.in_archive = True
		obj.save()
		messages.add_message(request, messages.INFO, 'Вакансия помещена в архив. На сайте она больше не отображается.')
		
	return HttpResponseRedirect(
		reverse('account_vacancy', args=[], kwargs={'username':request.user.username})
	)
	
##########################################################################
##########################################################################

@login_required
def resume_del(request, username, id):
	try:
		obj = Resume.activs.get(user=request.user, id=id)
	except:
		messages.add_message(request, messages.ERROR, 'Ошибка перемещения резюме в архив! Обратитесь к администратору.')
	else:
		obj.in_archive = True
		obj.save()
		messages.add_message(request, messages.INFO, 'Резюме помещено в архив. На сайте оно больше не отображается.')
		
	return HttpResponseRedirect(
		reverse('account_resume', args=[], kwargs={'username':request.user.username})
	)

##########################################################################
##########################################################################

##########################################################################
##########################################################################

@login_required
def vacancy_ret(request, username, id):
	try:
		obj = Vacancy.objects.filter(is_active=True, in_archive=True).get(user=request.user, id=id)#фильтр
	except:
		messages.add_message(request, messages.ERROR, 'Ошибка возврата вакансии из архива! Обратитесь к администратору.')
	else:
		obj.in_archive = False
		obj.save()
		messages.add_message(request, messages.INFO, 'Вакансия возвращена из архива. Она снова отображается на сайте.')

	return HttpResponseRedirect(
		reverse('account_vacancy', args=[], kwargs={'username':request.user.username})
	)

##########################################################################
##########################################################################

@login_required
def resume_ret(request, username, id):
	try:
		obj = Resume.objects.filter(is_active=True, in_archive=True).get(user=request.user, id=id)
	except:
		messages.add_message(request, messages.ERROR, 'Ошибка возврата резюме из архива! Обратитесь к администратору.')
	else:
		obj.in_archive = False
		obj.save()
		messages.add_message(request, messages.INFO, 'Резюме возвращено из архива. Оно сново отображается на сайте.')

	return HttpResponseRedirect(
		reverse('account_resume', args=[], kwargs={'username':request.user.username,})
	)

##########################################################################
##########################################################################

##########################################################################
##########################################################################

@login_required
@render_to('rabota/account_subscribe.html')
def account_subscribe(request, username):
	try: obj1 = SubscribeVacancy.activs.filter(user=request.user)[0]
	except: form1 = None
	else:
		form1 = AddVacancySubscribeForm(request.POST or None, instance=obj1)
		if form1.is_valid() and 'AddVacancySubscribeForm' in request.POST:
			form1.save()
			messages.add_message(request, messages.SUCCESS, u'Подписка на вакансии успешно сохранена.')
			return HttpResponseReload(request)
		
	try: obj2 = SubscribeResume.activs.filter(user=request.user)[0]
	except: form2 = None
	else:
		form2 = AddResumeSubscribeForm(request.POST or None, instance=obj2)
		if form2.is_valid() and 'AddResumeSubscribeForm' in request.POST:
			form2.save()
			messages.add_message(request, messages.SUCCESS, u'Подписка на резюме успешно сохранена.')
			return HttpResponseReload(request)
		
	return {
		'form1': form1,
		'form2': form2,
		'account_active': 4,
	}

##########################################################################
##########################################################################

##########################################################################
##########################################################################

class RegistrationCaptchView(RegistrationView):
	form_class = RegistrationCaptchaForm

@login_required
@render_to('registration/profile.html')
def account_profile(request, username):
	form1 = ProfileForm(request.POST or None, instance=request.user)
	if form1.is_valid():
		form1.save()
		messages.add_message(request, messages.SUCCESS, 'Данные сохранены.')
		return HttpResponseReload(request)

	form2 = PasswordChangeForm(request.user)

	return {
		'form1': form1,
		'form2': form2,
		'account_active': 1,
	}
	
@login_required
def account_change_password(request, username):
	if request.method == 'POST':
		form2 = PasswordChangeForm(user=request.user, data=request.POST)
		if form2.is_valid():
			form2.save()
			messages.add_message(request, messages.INFO, 'Пароль успешно изменен.')
			return HttpResponseRedirect(
				reverse('account_profile', args=[], kwargs={'username':username})
			)
		else:
			messages.add_message(request, messages.ERROR, 'Ошибка изменения пароля!')
			
		return HttpResponseRedirect(
			reverse('account_profile', args=[], kwargs={'username':username})
		)
		
	raise Http404()

##########################################################################
##########################################################################

##########################################################################
##########################################################################
