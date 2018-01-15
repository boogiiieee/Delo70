# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib import messages
from django.conf import settings

from threadmail import threading_send_mail

from feedback.models import FeedBackItem
from feedback.forms import FeedBackForm

################################################################################################################
################################################################################################################

def feedback_views(request, template, extra_context=None, context_processors=None, template_loader=loader):
	if request.method == 'POST':
		i = FeedBackItem()
		form = FeedBackForm(request.POST, instance=i)
		if form.is_valid():
			form.save()
			
			current_site = Site.objects.get_current()
			domain = current_site.domain
			
			users = User.objects.filter(is_staff=True, is_active=True)
			emails = [u.email for u in users]
			
			threading_send_mail('mail/feedback.html', u'Новое сообщение на сайте %s' % domain, emails, {'obj':i, 'domain':domain})
			
			messages.add_message(request, messages.INFO, u'Спасибо, Ваше сообщение отправлено!')
			return HttpResponseRedirect(request.META['HTTP_REFERER'])
	else:
		form = FeedBackForm()
		
	c = RequestContext(request, {'form':form, 'active':4,}, context_processors)
	
	if extra_context:
		for key, value in extra_context.items():
			if callable(value): c[key] = value()
			else: c[key] = value
			
	t = template_loader.get_template(template)
	return HttpResponse(t.render(c))
	
################################################################################################################
################################################################################################################