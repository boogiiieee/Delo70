# -*- coding: utf-8 -*-

from django.utils.encoding import smart_str
from django.utils.html import clean_html
from time import sleep
import re, os, sys
import datetime, random

from grab import Grab

from tools.parser import Price, find_email, find_phone, clean_str
		
######################################################################################################################
######################################################################################################################

def Parser(pages_count):
	u'''
		Парсер http://www.tomsk.ru/job/
	'''
	
	DEBUG = False
	p = Price()
	
	HREF = 'http://www.tomsk.ru'
	HREF_VACANCY = '/job/ajax/?&show=1&cat=vacancy'
	HREF_START = HREF + HREF_VACANCY + '&page=1'
	LOG_FILE = 'tomsk_ru.log'
	
	headers = {
		'Accept':'text/html, */*; q=0.01',
		'Accept-Encoding':'gzip,deflate,sdch',
		'Accept-Language':'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4',
		'Cache-Control':'max-age=0',
		'Connection':'keep-alive',
		'Host':'www.tomsk.ru',
		'Referer':'http://www.tomsk.ru/job/',
		'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.76 Safari/537.36',
		'X-Requested-With':'XMLHttpRequest',
	}
		
	def get_attr(g, name):
		try:
			return clean_str( g.doc.select(u'//div[contains(text(),"%s")]/../div[2]' % name).text() )
		except:
			return None

	g = Grab(headers=headers)
	g.setup(log_file=LOG_FILE, hammer_mode=True, hammer_timeouts=((2, 5), (10, 15), (20, 30)))
	
	def item_parser_r(x, deep):		
		if DEBUG:
			print 'deep=', deep
			print 'page=', x
		
		if pages_count and deep > pages_count:
			return
		
		g.go(x)
		
		next_url = HREF + HREF_VACANCY + '&page=' + str(deep + 1)
		
		items = g.tree.xpath(u'//a[contains(@href, "view")]/@href')
		# items = items[:2]
		
		for item in items:
			sleep( random.randint(3, 10) )
			
			print '.',
			
			if DEBUG: print 'item=', (HREF + item)
			
			g.go(HREF + item)
					
			x1 = get_attr(g, u'Должность:')
			x2 = get_attr(g, u'Cфера деятельности:')
			
			try:
				x3_tmp = get_attr(g, u'Зарплата:')
				x3 = u''
				pattern = re.compile(ur'[0-9 ]+', re.IGNORECASE | re.DOTALL)
				for i in pattern.findall(x3_tmp):
					tmp = re.sub(u'\D', u'', i) or None
					if tmp:
						x3 += (tmp + u',')
				if x3:
					x3 = x3[:-1]
				else:
					x3 = None
			except:
				x3 = None
			
			x4 = get_attr(g, u'Расписание:')
			
			try:
				x5 = clean_str( g.doc.select(u'//div[contains(text(),"Дополнительная информация:")]/following-sibling::div').text() )
			except:
				x5 = None
				
			try:
				x6 = clean_str( g.doc.select(u'//div[contains(text(),"Условия работы:")]/following-sibling::div').text() )
			except:
				x6 = None
				
			x7 = None
			try:
				tmp = clean_str( g.doc.select(u'//div[contains(text(),"Организация:")]/following-sibling::div').html() )
			except:
				tmp = None
			else:
				try:
					pattern = re.compile(ur'(\<div.class="clear.row">)(.+?)<br', re.IGNORECASE | re.DOTALL)
					x7 = clean_str( clean_html( pattern.findall(tmp)[0][1] ) )
				except:
					pass
					
			try:
				x8 = g.rex(re.compile(u'Имя:(.+?)<\/div')).group(1)
			except:
				x8 = None
				
			try:
				x9 = g.rex(re.compile(u'Email:.+?<a.+?>(.+?)<\/a>')).group(1)
			except:
				x9 = None
				
			try:
				x10 = g.rex(re.compile(u'Телефон:.+?<span.+?>(.+?)<\/span>')).group(1)
			except:
				x10 = None
				
			try:
				x11 = g.rex(re.compile(u'URL:.+?<a.+?>(.+?)<\/a>')).group(1)
			except:
				x11 = None
					
			x12 = HREF + item
			
			if x1 and x5:
				p.add(x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12)
			
			if DEBUG:
				print u'-------------------------'
				
				print u'Заголовок=', x1
				print u'Cфера деятельности=', x2
				print u'Зарплата=', x3
				print u'Расписание=', x4
				#print u'Дополнительная информация=', smart_str(x5)
				#print u'Условия работы=', smart_str(x6)
				print u'Организация=', x7
				print u'Имя=', x8
				print u'Email=', x9
				print u'Телефон=', x10
				print u'URL=', x11
				print u'Ссылка=', x12
				
				print u'-------------------------'
				
		if next_url:
			if DEBUG: print 'next_url=', next_url
			
			item_parser_r(next_url, deep+1)
			
	item_parser_r(HREF_START, 1)
	
	file_name = u'tomsk_ru_%s.xls' % datetime.datetime.now().strftime('%d%m%y%H%M%S')
	if DEBUG: print file_name
		
	title = [
		u'Заголовок',
		u'Cфера деятельности',
		u'Зарплата', 
		u'Расписание', 
		u'Дополнительная информация', 
		u'Условия работы', 
		u'Организация', 
		u'Имя', 
		u'Email', 
		u'Телефон', 
		u'URL',
		u'Ссылка',
	]
	p.save(title, file_name)
	
	return 1
	
######################################################################################################################
######################################################################################################################

if __name__ == "__main__":
	u'''
		http://www.tomsk.ru/job/
		tomsk_ru.py [count]
		count - Необязательный параметр. Количество страниц, которое требуется обработать.
		Если count = 0 или не указан, то будут обработаны все страницы.
	'''
	
	pages_count = None
	
	if len(sys.argv) == 2: pages_count = int(sys.argv[1])
	
	Parser(pages_count)
	
######################################################################################################################
######################################################################################################################