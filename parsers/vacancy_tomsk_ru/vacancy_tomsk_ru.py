# -*- coding: utf-8 -*-

import re, os, sys
import datetime

from grab import Grab

from tools.parser import Price, find_email, find_phone, clean_str
		
######################################################################################################################
######################################################################################################################

def Parser(pages_count):
	u'''
		Парсер http://vacancy.tomsk.ru/
	'''
	
	DEBUG = False
	p = Price()
	
	HREF = 'http://vacancy.tomsk.ru'
	HREF_START = '%s/index.php?start=0' % HREF
	LOG_FILE = 'vacancy_tomsk_ru.log'
		
	def get_attr(g, x):
		try:
			return clean_str( g.tree.xpath(u'//*[contains(text(), "%s")]/../..//td[2]/text()' % x)[0] )
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
		
		try: next_url = HREF + g.doc.select(u'//a[contains(text(), "Следующая")]/@href').text()
		except: next_url = None
		
		items = g.tree.xpath(u'//*[contains(text(), "подробнее")]/@href')
		#items = items[:2]
		
		for item in items:
			print '.',
			
			if DEBUG: print 'item=', (HREF + item)
			
			g.go(HREF + item)
					
			x0 = g.tree.xpath(u'//*[@id="mcontent"]//h3/text()')[0]
			x0 = clean_str( x0.lower().capitalize() )
			
			x1 = get_attr(g, u'Занятость')
			x2 = get_attr(g, u'Сфера деятельности')
			
			x3 = None
			tmp = get_attr(g, u'Ориентировочная зарплата')
			tmp2 = []
			if tmp:
				for i in re.findall(u'[\d ,]+', tmp):
					if i:
						try: tmp1 = float(re.sub(ur'\D', u'', i))
						except: pass
						else:
							if tmp1 and tmp1 > 999.0:
								tmp2 += [u'%.2f' % tmp1]
				if tmp2: x3 = u', '.join(tmp2)
			
			x4 = get_attr(g, u'Уровень образования')
			x5 = get_attr(g, u'Уровень опыта')
			
			try: x6 = clean_str( g.tree.xpath(u'//*[contains(text(), "Название компании")]/../..//td/a/text()')[0] )
			except: x6 = None
			
			try: x7 = g.doc.select(u'//*[@id="mcontent"]/table[2]')[0].text()
			except: x7 = None
			
			x8 = None
			tmp = find_phone(x7)
			if tmp:
				x8 = u', '.join(tmp)
			
			x9 = None
			tmp = find_email(x7)
			if tmp: x9 = u', '.join(tmp)
			
			x10 = HREF + item
			
			try: x11 = clean_str( g.doc.select(u'//*[contains(text(), "Действительно с")]/../../td')[0].text() )
			except: x11 = None
			
			if x11:
				tmp = re.findall(ur'\d{4}\-\d{2}\-\d{2}', x11)
				if tmp: x11 = tmp[0]
			
			p.add(x0, x11, x1, x2, x3, x4, x5, x6, x7, x8, x9, x10)
			
			if DEBUG:
				print u'-------------------------'
				
				print u'Заголовок=', x0
				print u'Дата=', x11
				print u'Занятость=', x1
				print u'Сфера деятельности=', x2
				print u'Ориентировочная зарплата=', x3
				print u'Уровень образования=', x4
				print u'Уровень опыта=', x5
				print u'Название компании=', x6
				print u'Текст=', x7
				print u'Телефоны=', x8
				print u'E-mail=', x9
				print u'Ссылка=', x10
				
				print u'-------------------------'
				
		if next_url:
			if DEBUG: print 'next_url=', next_url
			
			item_parser_r(next_url, deep+1)
			
	item_parser_r(HREF_START, 1)
	
	file_name = u'vacancy_tomsk_ru_%s.xls' % datetime.datetime.now().strftime('%d%m%y%H%M%S')
	if DEBUG: print file_name
		
	title = [
		u'Заголовок',
		u'Дата',
		u'Занятость', 
		u'Сфера деятельности', 
		u'Ориентировочная зарплата', 
		u'Уровень образования', 
		u'Уровень опыта', 
		u'Название компании', 
		u'Текст', 
		u'Телефоны', 
		u'E-mail',
		u'Ссылка',
	]
	p.save(title, file_name)
	
	return 1
	
######################################################################################################################
######################################################################################################################

if __name__ == "__main__":
	u'''
		http://vacancy.tomsk.ru
		vacancy_tomsk_ru.py [count]
		count - Необязательный параметр. Количество страниц, которое требуется обработать.
		Если count = 0 или не указан, то будут обработаны все страницы.
	'''
	
	pages_count = None
	
	if len(sys.argv) == 2: pages_count = int(sys.argv[1])
	
	Parser(pages_count)
	
######################################################################################################################
######################################################################################################################