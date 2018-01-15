# -*- coding: utf-8 -*-

from django.db import transaction
from django.utils.text import capfirst
from django.utils.encoding import smart_str
from django.conf import settings
import datetime
import re, os, sys

from pytils.translit import slugify
import xlrd

from annoying.functions import get_object_or_None

from geo.models import CustomLocation
from rabota.models import Schedule, TypeEmployment, TypeWages, Education, Experience, Category, Vacancy, Resume, SubscribeVacancy, SubscribeResume

from parsers.file_parser.callbacks.choice import SCHEDULE_CHOICE, TYPE_EMPLOYMENT_CHOICE, EDUCATION_CHOICE, EXPERIENCE_CHOICE, CATEGORY_CHOICE					
from parsers.file_parser.callbacks.utils import get_attr_fk

DEBUG = False
PATH = os.path.dirname(settings.MEDIA_ROOT)
NOT = u'Не указано'

################################################################################################################
################################################################################################################

################################################################################################################
################################################################################################################

# print u'Заголовок=', smart_str(x0)
# print u'Зарплата=', smart_str(x1)
# print u'Контактное лицо=', smart_str(x2)
# print u'Название компании=', smart_str(x3)
# print u'Город=', smart_str(x4)
# print u'Текст=', smart_str(x5)
# print u'Сфера деятельности=', smart_str(x6)
# print u'График работы=', smart_str(x7)
# print u'Телефон=', smart_str(x8)

@transaction.commit_on_success
def ImportFile(file, city_id):

	file = os.path.normpath(os.path.join(PATH, '%s') % file)
	result, count_item, errors_item = True, 0, u''
	
	if DEBUG: print 'file=', file
	
	try:
		f = open(file, 'rb')
		rb = xlrd.open_workbook(file_contents=f.read())
		sheet = rb.sheet_by_index(0)
		
		for rownum in range(1, sheet.nrows):
			count_item += 1
			
			cols = sheet.row_values(rownum)
			
			if cols:
				x0 = cols[0].strip()
				
				x1 = [0, 0]
				try: x1[0] = float(cols[1])
				except: pass
				
				x2 = cols[2] or NOT
				x3 = cols[3] or NOT
				
				x4 = CustomLocation.objects.get( id=city_id )
				
				x5 = cols[5]
				
				x6, errors_item = get_attr_fk(Category, CATEGORY_CHOICE, cols[6], errors_item)
				if not x6:
					x6 = Category.activs.get(pk=38)
					
				x7, errors_item = get_attr_fk(TypeEmployment, TYPE_EMPLOYMENT_CHOICE, cols[7], errors_item)
				x9, errors_item = get_attr_fk(Schedule, SCHEDULE_CHOICE, cols[7], errors_item)
				
				x8 = cols[8]
				
				if x0 and x5 and x8:				
					v = Vacancy.objects.filter(user=None, post=x0, brief=x8[:250], company=x7, fio=x2, phone1=x8).count()

					if not v:
						v = Vacancy.objects.create(
							user = None,
							post = x0,
							brief = x5[:250],
							schedule = x9,
							type_employment = x7,
							wage_min = x1[0] if x1[0] else None,
							wage_max = x1[1] if x1[1] else None,
							type_wages = TypeWages.objects.get_or_create(pk=1)[0],
							description = x5,
							company = x3,
							fio = x2,
							phone1 = x8,
							city = x4,
							is_active = True,
						)

						v.category.add(x6)
							
				
					if DEBUG:
						print u'-------------------------'
						
						print u'Заголовок=', x0
						print u'Зарплата=', x1
						print u'Контактное лицо=', x2
						print u'Название компании=', x3
						print u'Город=', x4
						print u'Текст=', smart_str(x5)
						print u'Сфера деятельности=', x6
						print u'Тип занятости=', x7
						print u'График работы=', x9
						print u'Телефон=', x8
						
						print u'-------------------------'
			
	except:
		e = sys.exc_info()
		if DEBUG: print 'errors =', e
		result = False
	
	return [result, count_item, errors_item]
	
################################################################################################################
################################################################################################################
	
################################################################################################################
################################################################################################################