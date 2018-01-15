# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext, Context
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.models import User
from django.contrib.sites.models import Site

try:
	import  json
except:
	import simplejson as json

from threadmail import threading_send_mail

from complaint.models import Complaints
from complaint.forms import ComplaintForm



#Вьюшка, которая обрабатывает запрос на запись замечания в базу


def api_get_concert(request, use_https=False):
				 protokol = u'https' if use_https else u'http'
				 return protokol
@csrf_exempt
def	get_complaint(request):
	if request.is_ajax() and request.method == 'POST':
		form = ComplaintForm(request.POST)
		if form.is_valid():
			comp = form.cleaned_data
			message = comp['message'][:200]
			url = request.POST['url']
			complaint_item = Complaints.objects.create(url = url, text = message)
			
			users = User.objects.filter(is_staff=True, is_active=True)
			emails = [u.email for u in users]
			domain = Site.objects.get_current().domain	
			protokol = api_get_concert(request)

			link = u'%(protokol)s://%(domain)s/admin/complaint/complaints/%(id)d/' % {'protokol' : protokol, 'domain' : domain, 'id' : complaint_item.id}		

			if emails:
				threading_send_mail('mail/complaint_subscribe.html', u'Новое сообщение об ошибке', emails, {'url' : url, 'text' : message, 'link' : link, 'domain' : domain })

			return HttpResponse( json.dumps( {} ), mimetype="application/json" )
	else:
		return HttpResponse(status=400)

		