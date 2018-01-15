# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('clear_cache.views',
	url(r'^clear_cache/$', 'clear_cache_views'),
)