# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext

from configuration.views import get_config

##################################################################################################	
##################################################################################################

class ConfigurationMiddleware(object):
	def process_request(self, request):
		request.config = get_config()
		
	def process_response(self, request, response):
		if hasattr(request, 'config'):
			config = request.config
		else:
			config = get_config()
			
		if not config.is_active:
			return render_to_response('off.html', {}, RequestContext(request))
		return response
			
##################################################################################################	
##################################################################################################