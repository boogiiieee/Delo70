# -*- coding: utf-8 -*-

from django.db import transaction
from django.utils.text import capfirst
from django.utils.encoding import smart_str
from django.conf import settings
import datetime
import urllib
import urllib2
import re, os, sys
import json

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

# u'Заголовок=', 0+
# u'Дата=', 1+
# u'Адрес=', 2+
# u'Ориентировочная зарплата=', 3+
# u'Условия=', 4+
# u'Описание=', 5+
# u'Навыки и опыт=', 6+
# u'Контактное лицо=', 7+
# u'Организация=', 8+
# u'Телефон=', 9+
# u'E-mail=', 10+

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
						
				try: x1 = datetime.datetime.strptime(cols[1], '%Y-%m-%d')
				except: x1 = None
					
				x2, errors_item = get_attr_fk(TypeEmployment, TYPE_EMPLOYMENT_CHOICE, cols[4], errors_item)
				x3, errors_item = get_attr_fk(Category, CATEGORY_CHOICE, cols[0]+cols[5]+cols[6]+cols[4], errors_item, list_num=2)
				
				if not x3:
					x3 = Category.activs.get(pk=38)
					
				x4 = [None, None]
				try: tmp = cols[3].split(u',')
				except: pass
				else:
					try: x4[0] = float(tmp[0])
					except: pass
					
					try: x4[1] = float(tmp[1])
					except: pass
					
				x5, errors_item = get_attr_fk(Education, EDUCATION_CHOICE, cols[4], errors_item)
				x6, errors_item = get_attr_fk(Experience, EXPERIENCE_CHOICE, cols[4], errors_item)
				x14, errors_item = get_attr_fk(Schedule, SCHEDULE_CHOICE, cols[4], errors_item)
					
				x7 = cols[8] or NOT
				x8 = cols[5] or NOT
				x13 = cols[6] or u''
				
				x9 = [u'', u'']
				try: tmp = cols[9].split(u',')
				except: pass
				else:
					try:
						if tmp[0]: x9[0] = tmp[0].strip()
					except: pass
					
					try:
						if tmp[1]: x9[1] = tmp[1].strip()
					except: pass
						
				x10 = cols[10].split(u',') if cols[10] else [NOT]
				x11 = cols[7] or u''
				
				x12 = CustomLocation.objects.get( id=city_id )
				
				v = Vacancy.objects.filter(user=None, post=x0, brief=x8[:250], company=x7).count()

				if not v and (x9[0].strip() or x9[1].strip() or x10[0].strip()):
					v = Vacancy.objects.create(
						user = None,
						post = x0,
						brief = x8[:250],
						schedule = x14,
						type_employment = x2,
						wage_min = x4[0] if x4[0] else None,
						wage_max = x4[1] if x4[1] else None,
						type_wages = TypeWages.objects.get_or_create(pk=1)[0],
						description = x8,
						education = x5,
						experience = x6,
						professional_skills = x13,
						company = x7,
						fio = x11,
						phone1 = x9[0].strip(),
						phone2 = x9[1].strip(),
						email = x10[0].strip(),
						city = x12,
						is_active = True,
					)

					v.category.add(x3)
						
			
				if DEBUG:
					print u'-------------------------'
					
					print u'Заголовок=', x0
					print u'Дата=', x1
					print u'Занятость=', x2
					print u'Сфера деятельности=', x3
					print u'Ориентировочная зарплата=', x4
					print u'Уровень образования=', x5
					print u'Уровень опыта=', x6
					#print u'Название компании=', smart_str(x7)
					#print u'Другие условия=', smart_str(x8)
					#print u'Другие требования=', smart_str(x13)
					print u'Телефоны=', x9
					print u'E-mail=', x10
					print u'Контактное лицо=', x11
					print u'Адрес=', smart_str(x12)
					print u'График работы=', x14
					
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