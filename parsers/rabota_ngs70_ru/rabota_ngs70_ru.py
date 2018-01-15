# -*- coding: utf-8 -*-

import re, os, sys
import datetime

from grab import Grab

from tools.parser import Price, find_email, find_phone, clean_str
		
######################################################################################################################
######################################################################################################################

def Parser(pages_count):
	u'''
		Парсер http://rabota.ngs70.ru/
	'''
	
	DEBUG = False
	p = Price()
	
	HREF = 'http://rabota.ngs70.ru'
	HREF_VACANCY = '/vacancy'
	HREF_START = HREF + HREF_VACANCY + '?q='
	LOG_FILE = 'rabota_ngs70_ru.log'
		
	def get_attr(g, x):
		try:
			return clean_str( g.doc.select(u'//*[@class="%s"]' % x)[0].text() )
		except:
			return None

	g = Grab()
	g.setup(log_file=LOG_FILE, hammer_mode=True, hammer_timeouts=((2, 5), (10, 15), (20, 30)))
	
	def item_parser_r(x, deep):
		if DEBUG:
			print 'deep=', deep
			print 'page=', x
		
		if pages_count and deep > pages_count:
			return
		
		g.go(x)
		
		try: next_url = HREF + HREF_VACANCY + g.doc.select(u'//span[contains(text(), "следующая")]/../@href').text()
		except: next_url = None
		
		items = g.tree.xpath(u'//a[@class="ra-elements-list__new-window-link"]/@href')
		#items = items[:2]
		
		for item in items:
			print '.',
			
			if DEBUG: print 'item=', (HREF + HREF_VACANCY + item)
			
			g.go(HREF + HREF_VACANCY + item)
					
			x1 = g.doc.select(u'//div[@class="ra-vacancy-full-title"]/h2')[0].text()
			x2 = get_attr(g, u'ra-vacancy-full-info-data-post')
			x3 = get_attr(g, u'ra-vacancy-full-location')
			
			x4 = None
			try:
				tmp = get_attr(g, u'ra-vacancy-full-salary')
				if tmp:
					tmp = [u'%.2f' % float(i.replace(u' ', u'')) for i in re.findall(ur'[\d ]+', tmp)]
					if tmp:
						x4 = u', '.join(tmp)
			except:
				pass
			
			try:
				x5 = [clean_str( i.text() ) for i in g.doc.select(u'//li[@class="ra-vacancy-full-requirements-list-item"]')] or None
				if x5:
					x5 = u'. '.join(x5)
			except:
				x5 = None
				
			x6 = get_attr(g, u'ra-vacancy-full-description-text')
			
			x7 = get_attr(g, u'ra-vacancy-full-skills')
			if x7:
				x7 = clean_str( x7.replace(u'Навыки и опыт', u'') )
				
			x8 = get_attr(g, u'ra-vacancy-full-contact-info-person')
			x9 = get_attr(g, u'ra-vacancy-full-contact-info-company')
			x10 = get_attr(g, u'ra-vacancy-full-contact-info-phone')
			
			x11 = None
			try:
				tmp = clean_str( g.doc.select(u'//*[@class="ra-vacancy-full-contact-info-mail"]')[0].text() )
				if tmp:
					tmp = find_email(tmp)
					if tmp:
						x11 = u', '.join(tmp)
			except:
				pass
					
			x12 = HREF + HREF_VACANCY + item
			
			p.add(x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12)
			
			if DEBUG:
				print u'-------------------------'
				
				print u'Заголовок=', x1
				print u'Дата=', x2
				print u'Адрес=', x3
				print u'Ориентировочная зарплата=', x4
				#print u'Условия=', x5
				#print u'Описание=', x6
				print u'Навыки и опыт=', x7
				print u'Контактное лицо=', x8
				print u'Организация=', x9
				print u'Телефон=', x10
				print u'E-mail=', x11
				print u'Ссылка=', x12
				
				print u'-------------------------'
				
		if next_url:
			if DEBUG: print 'next_url=', next_url
			
			item_parser_r(next_url, deep+1)
			
	item_parser_r(HREF_START, 1)
	
	file_name = u'rabota_ngs70_ru_%s.xls' % datetime.datetime.now().strftime('%d%m%y%H%M%S')
	if DEBUG: print file_name
		
	title = [
		u'Заголовок',
		u'Дата',
		u'Адрес', 
		u'Ориентировочная зарплата', 
		u'Условия', 
		u'Описание', 
		u'Навыки и опыт', 
		u'Контактное лицо', 
		u'Организация', 
		u'Телефон', 
		u'E-mail',
		u'Ссылка',
	]
	p.save(title, file_name)
	
	return 1
	
######################################################################################################################
######################################################################################################################

if __name__ == "__main__":
	u'''
		http://rabota.ngs70.ru
		rabota_ngs70_ru.py [count]
		count - Необязательный параметр. Количество страниц, которое требуется обработать.
		Если count = 0 или не указан, то будут обработаны все страницы.
	'''
	
	pages_count = None
	
	if len(sys.argv) == 2: pages_count = int(sys.argv[1])
	
	Parser(pages_count)
	
######################################################################################################################
######################################################################################################################