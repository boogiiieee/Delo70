# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url

#Форма отправки сообщения об ошибке

urlpatterns = patterns('complaint.views',
	url(r'$', 'get_complaint', name='get_complaint'),
)