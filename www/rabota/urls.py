# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url
from django.http import HttpResponsePermanentRedirect

urlpatterns = patterns('rabota.views',
	url(r'^vacancy/item/(?P<id>[0-9]+)/(?P<slug>.+)/$', lambda request, id, slug: HttpResponsePermanentRedirect('/tomsk/vacancy/item/%s/%s/' % (id, slug))),
	
	url(r'^$', 'index', name='index'),
	url(r'^contacts/$', 'contacts', name='contacts'),
	
	
	url(r'^(?P<slug_city>[\w-]+)/vacancy/$', 'vacancy', name='vacancy'),
	url(r'^(?P<slug_city>[\w-]+)/resume/$', 'resume', name='resume'),

	url(r'^(?P<slug_city>[\w-]+)/vacancy/(?P<id>[0-9]+)/$', 'vacancy_item', name='vacancy_item_old'),
	url(r'^(?P<slug_city>[\w-]+)/resume/(?P<id>[0-9]+)/$', 'resume_item', name='resume_item_old'),
	
	url(r'^(?P<slug_city>[\w-]+)/vacancy/item/(?P<id>[0-9]+)/(?P<slug>.+)/$', 'vacancy_item', name='vacancy_item'),
	url(r'^(?P<slug_city>[\w-]+)/resume/item/(?P<id>[0-9]+)/(?P<slug>.+)/$', 'resume_item', name='resume_item'),
	
	url(r'^(?P<slug_city>[\w-]+)/vacancy/category/item/(?P<ct>[0-9]+)/(?P<id>[0-9]+)/(?P<slug>.+)/$', 'vacancy_item', name='vacancy_category_item'),
	url(r'^(?P<slug_city>[\w-]+)/resume/category/item/(?P<ct>[0-9]+)/(?P<id>[0-9]+)/(?P<slug>.+)/$', 'resume_item', name='resume_category_item'),
	
	url(r'^(?P<slug_city>[\w-]+)/vacancy/category/(?P<id>[0-9]+)/(?P<slug>.+)/$', 'category_vacancy', name='category_vacancy_url'),
	url(r'^(?P<slug_city>[\w-]+)/resume/category/(?P<id>[0-9]+)/(?P<slug>.+)/$', 'category_resume', name='category_resume_url'),
	
	url(r'^(?P<slug_city>[\w-]+)/vacancy/search/$', 'vacancy_search', name='vacancy_search'),
	url(r'^(?P<slug_city>[\w-]+)/vacancy/advanced-search/$', 'vacancy_search_advanced', name='vacancy_search_advanced'),
	url(r'^(?P<slug_city>[\w-]+)/resume/search/$', 'resume_search', name='resume_search'),
	url(r'^(?P<slug_city>[\w-]+)/resume/advanced-search/$', 'resume_search_advanced', name='resume_search_advanced'),
	
	url(r'^(?P<slug_city>[\w-]+)/vacancy/add/$', 'vacancy_add', name='vacancy_add'),
	url(r'^(?P<slug_city>[\w-]+)/resume/add/$', 'resume_add', name='resume_add'),
	
	
	url(r'^vacancy/subscribe/add/$', 'vacancy_subscribe_add', name='vacancy_subscribe_add'),
	url(r'^resume/subscribe/add/$', 'resume_subscribe_add', name='resume_subscribe_add'),
	
	url(r'^vacancy/subscribe/del/$', 'vacancy_subscribe_del', name='vacancy_subscribe_del'),
	url(r'^resume/subscribe/del/$', 'resume_subscribe_del', name='resume_subscribe_del'),
	
	url(r'^users/(?P<username>[a-zA-Z0-9@.+-_]+)/vacancy/$', 'account_vacancy', name='account_vacancy'),
	url(r'^users/(?P<username>[a-zA-Z0-9@.+-_]+)/resume/$', 'account_resume', name='account_resume'),
	
	url(r'^users/(?P<username>[a-zA-Z0-9@.+-_]+)/vacancy/(?P<id>[0-9]+)/$', 'account_vacancy_item', name='account_vacancy_item'),
	url(r'^users/(?P<username>[a-zA-Z0-9@.+-_]+)/resume/(?P<id>[0-9]+)/$', 'account_resume_item', name='account_resume_item'),
	
	url(r'^users/(?P<username>[a-zA-Z0-9@.+-_]+)/vacancy/(?P<id>[0-9]+)/del/$', 'vacancy_del', name='vacancy_del'),
	url(r'^users/(?P<username>[a-zA-Z0-9@.+-_]+)/resume/(?P<id>[0-9]+)/del/$', 'resume_del', name='resume_del'),

	url(r'^users/(?P<username>[a-zA-Z0-9@.+-_]+)/vacancy/(?P<id>[0-9]+)/ret/$', 'vacancy_ret', name='vacancy_ret'),
	url(r'^users/(?P<username>[a-zA-Z0-9@.+-_]+)/resume/(?P<id>[0-9]+)/ret/$', 'resume_ret', name='resume_ret'),
	
	url(r'^account/(?P<username>[a-zA-Z0-9@.+-_]+)/subscribe/$', 'account_subscribe', name='account_subscribe'),
	
	url(r'^users/(?P<username>[a-zA-Z0-9@.+-_]+)/change-password/$', 'account_change_password', name='account_change_password'),
	url(r'^users/(?P<username>[a-zA-Z0-9@.+-_]+)/$', 'account_profile', name='account_profile'),
)
