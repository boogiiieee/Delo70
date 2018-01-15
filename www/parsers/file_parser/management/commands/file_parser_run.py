# -*- coding: utf-8 -*-

from django.core.management.base import NoArgsCommand
import datetime
import os, re

from configuration.views import get_config

from parsers.file_parser.models import Uploader, File
	
#######################################################################################################################
#######################################################################################################################

class Command(NoArgsCommand):
	help = u"Запустить загрузчик"

	def handle_noargs(self, **options):
	
		if File.objects.filter(status='1').count() == 0:
			config = get_config()
			config.is_active = False
			config.save()
			
			try:
				for f in File.objects.filter(status='0').order_by('id'):
				
					f.errors = u'Парсер начал загрузку прайс-листа.\n'
					f.status = '1'
					f.date_start = datetime.datetime.now()
					f.save()
					
					result, count_item, errors_item = False, 0, u''

					try:
						cb = str(f.uploader.callback).split('.')
						cb_function = cb[-1]
						cb_import = 'from ' + '.'.join(cb[:-1]) + ' import ' + cb_function

						exec(cb_import)
					except:
						errors_item += u'Ошибка подключения загрузчика.\n'
					else:
						exec( 'result, count_item, errors_item = %s("%s", %d)' % (cb_function, f.file.url, f.city.id) )
					
					f.errors += u'Парсер завершил загрузку прайс-листа.\n'
					f.status = '2' if result == True else '3'
					f.count_item = count_item
					f.errors += errors_item
					f.date_end = datetime.datetime.now()
					f.save()
			except:
				pass
				
			config.is_active = True
			config.save()
				
		return

#######################################################################################################################
#######################################################################################################################
