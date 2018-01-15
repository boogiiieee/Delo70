# -*- coding: utf-8 -*-

from django.core.management.base import NoArgsCommand
from django.contrib.sites.models import Site
import datetime

from rabota.models import Vacancy, Resume, SubscribeVacancy, SubscribeResume
from threadmail import threading_send_mail
	
#######################################################################################################################
#######################################################################################################################

class Command(NoArgsCommand):
	help = "Send subscribe"

	def handle_noargs(self, **options):
		try:
			file = open('send_subscribe.txt', 'r')
			dt = datetime.datetime.strptime(file.read(), '%d.%m.%Y %H:%M:%S')
			file.close()
		except:
			dt = None
			
		SubscribeVacancy.objects.filter(modified__lte=datetime.datetime.now()-datetime.timedelta(days=30)).delete()
		SubscribeResume.objects.filter(modified__lte=datetime.datetime.now()-datetime.timedelta(days=30)).delete()
			
		if dt:
			current_site = Site.objects.get_current()
			domain = current_site.domain
				
			for item in SubscribeVacancy.activs.all():
				email = item.user.email
				if email:
					items = Vacancy.activs.filter(created__gte=dt)
					
					query = {'city':item.city}
					if item.category.all(): query['category__id__in'] = item.category.all()
					if item.schedule: query['schedule'] = item.schedule
					if item.type_employment: query['type_employment'] = item.type_employment
					if item.wage_min: query['wage_min__gte'] = item.wage_min
					if item.wage_max: query['wage_max__lte'] = item.wage_max
					if item.type_wages: query['type_wages'] = item.type_wages
					if item.education: query['education'] = item.education
					if item.experience: query['experience'] = item.experience
					
					if query:
						items = items.filter(**query)
					items = items.distinct()[:10]
						
					if items:
						threading_send_mail('rabota/mail/vacansy_subscribe.html', u'Новые вакансии на сайте %s' % domain, [email], {'items':items[:10], 'domain':domain})
					
			for item in SubscribeResume.activs.all():
				email = item.user.email
				if email:
					items = Resume.activs.filter(created__gte=dt)
					
					query = {'city':item.city}
					if item.category.all(): query['category__id__in'] = item.category.all()
					if item.schedule: query['schedule'] = item.schedule
					if item.type_employment: query['type_employment'] = item.type_employment
					if item.wage_min: query['wage_min__gte'] = item.wage_min
					if item.type_wages: query['type_wages'] = item.type_wages
					if item.experience: query['experience'] = item.experience
					if item.education: query['education'] = item.education
					
					if query:
						items = items.filter(**query)
					items = items.distinct()[:10]
						
					if items:
						threading_send_mail('rabota/mail/resume_subscribe.html', u'Новые резюме на сайте %s' % domain, [email], {'items':items, 'domain':domain})
						
		file = open('send_subscribe.txt', 'w')
		file.write(datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S'))
		file.close()
		
		return

#######################################################################################################################
#######################################################################################################################
