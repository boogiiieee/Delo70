# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect, Http404
from django.contrib import messages

################################################################################################################
################################################################################################################

def clear_cache_views(request):
	if request.user.is_superuser:
		from clear_cache import clearcache
		clearcache()
		messages.add_message(request, messages.INFO, u'Кэш очищен.')
		
		if 'HTTP_REFERER' in request.META and request.META['HTTP_REFERER']:
			return HttpResponseRedirect(request.META['HTTP_REFERER'])
		return HttpResponseRedirect('/admin/')
	return Http404()
	
################################################################################################################
################################################################################################################