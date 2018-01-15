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

# print u'Заголовок=', x1
# print u'Cфера деятельности=', x2
# print u'Зарплата=', x3
# print u'Расписание=', x4
# print u'Дополнительная информация=', smart_str(x5)
# print u'Условия работы=', smart_str(x6)
# print u'Организация=', x7
# print u'Имя=', x8
# print u'Email=', x9
# print u'Телефон=', x10
# print u'URL=', x11
# print u'Ссылка=', x12

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
				x1 = cols[0].strip()
				
				x2, errors_item = get_attr_fk(Category, CATEGORY_CHOICE, cols[1], errors_item)
				if not x2:
					x2 = Category.activs.get(pk=38)

				x3 = [0, 0]
				try: x3[0] = float(cols[2])
				except: pass
				
				x4, errors_item = get_attr_fk(TypeEmployment, TYPE_EMPLOYMENT_CHOICE, cols[3], errors_item)
				x5, errors_item = get_attr_fk(Schedule, SCHEDULE_CHOICE, cols[3], errors_item)
				
				x6 = cols[4] or NOT
				x7 = cols[5] or NOT
				
				x8 = cols[6] or NOT
				x9 = cols[7] or NOT
				x10 = cols[8]
				x11 = cols[9] or NOT
				x12 = cols[10]
				
				x13 = CustomLocation.objects.get( id=city_id )
				
				if x1 and x6:				
					v = Vacancy.objects.filter(user=None, post=x1, brief=x6[:250], company=x8, fio=x9, phone1=x11, email=x10).count()

					if not v and (x11 or x10):
						v = Vacancy.objects.create(
							user = None,
							post = x1,
							brief = x6[:250],
							schedule = x5,
							type_employment = x4,
							wage_min = x3[0] if x1[0] else None,
							wage_max = x3[1] if x1[1] else None,
							type_wages = TypeWages.objects.get_or_create(pk=1)[0],
							description = x6 + u' ' + x7,
							company = x8,
							fio = x9,
							phone1 = x11,
							email = x10,
							site = x12,
							city = x13,
							is_active = True,
						)

						v.category.add(x2)
							
				
					if DEBUG:
						print u'-------------------------'
						
						print u'Заголовок=', x1
						print u'Cфера деятельности=', x2
						print u'Зарплата=', x3
						print u'Тип занятости=', x4
						print u'График работы=', x5
						print u'Дополнительная информация=', smart_str(x6)
						print u'Условия работы=', smart_str(x7)
						print u'Организация=', x8
						print u'Имя=', x9
						print u'Email=', x10
						print u'Телефон=', x11
						print u'URL=', x12
						
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