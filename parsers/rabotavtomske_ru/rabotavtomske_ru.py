# -*- coding: utf-8 -*-

import re, os, sys
import datetime

from grab import Grab

try:
	import Image
	import ImageDraw
	import ImageFont
except ImportError:
	from PIL import Image, ImageDraw, ImageFont

from tools.parser import Price, find_email, find_phone, clean_str
		
######################################################################################################################
######################################################################################################################

def Parser(pages_count):
	'''
		Парсит сайт http://rabotavtomske.ru.
		Результат сохраняет в exel файлы.
	'''
	
	DEBUG = False
	p = Price()
	
	HREF = 'http://rabotavtomske.ru'
	HREF_START = HREF + '/vacancies/'
	LOG_FILE = 'rabotavtomske_ru.log'
	
	g = Grab()
	g.setup(log_file=LOG_FILE, hammer_mode=True, hammer_timeouts=((2, 5), (10, 15), (20, 30)))
	
	def get_attr(g, name):
		try:
			return clean_str( g.doc.select(u'//td[contains(text(),"%s")]/../td[3]' % name).text() )
		except:
			return None
	
	def item_parser_r(x, deep):
		if DEBUG:
			print 'deep=', deep
			print 'page=', x
		
		if pages_count and deep > pages_count:
			return
			
		g.go(x)
		
		try: next_url = HREF_START + g.doc.select(u'//a[text()="следующая"]/@href').text()
		except: next_url = None
		
		items = g.tree.xpath(u'//a[@class="vacname"]/@href')
		#items = items[1:2]
	
		for item in items:
			print '.',
			
			if DEBUG: print 'item=', (HREF + item)
			
			g.go(HREF + item)
			
			x1 = g.doc.select(u'//h1').text().capitalize()
			x2 = g.doc.select(u'//td[contains(text(),"Категория вакансии")]/../td[3]').text()
			x3 = g.doc.select(u'//td[contains(text(),"Дата добавления")]/../td[3]').text()
			
			x4 = get_attr(g, u'Заработная плата')
			x5 = get_attr(g, u'График работы')
			x6 = get_attr(g, u'Другие условия')
			
			x7 = get_attr(g, u'Пол')
			x8 = get_attr(g, u'Возраст')
			
			x9 = get_attr(g, u'Образование')
			x10 = get_attr(g, u'Стаж')
			x11 = get_attr(g, u'Другие требования')
			
			x12 = get_attr(g, u'Регион')
			x13 = get_attr(g, u'Название')
			
			tmp = get_attr(g, u'Телефон')
			x14 = [tmp] if tmp else None
			
			tmp = get_attr(g, u'E-mail')
			x15 = [tmp] if tmp else None
			
			x16 = get_attr(g, u'Адрес сайта')
			x17 = get_attr(g, u'Адрес')
			
			x18 = HREF + item
			
			text = (x6 or u'') + (x11 or u'')
			
			if not x14:
				tmp = find_phone(text)
				if tmp:
					x14 = u', '.join(tmp)
			
			if not x15:
				tmp = find_email(text)
				if tmp:
					x15 = u', '.join(tmp)
					
			# try:
				# tmp = g.doc.select(u'//td[contains(text(),"E-mail")]/../td[3]//img/@src').text()
			# except:
				# tmp = None
			# else:
				# tmp = tmp.replace(u'..', u'')
			
				# g.go(HREF + tmp)
				# g.response.save('tmp.png')
				
				# img = Image.open('tmp.png')
				# width, height = img.size
				# img_resize = img.resize(((width/height) * (height*2), height*2), Image.BILINEAR)
				# img_resize.save('tmp_resize.png', dpi=(300,300), format="PNG")
			
			p.add(x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13, x14, x15, x16, x17, x18)
			
			if DEBUG:
				print u'-------------------------'
				
				print u'Заголовок=', x1
				print u'Категория вакансии=', x2
				print u'Дата=', x3
				print u'Заработная плата=', x4
				print u'График работы=', x5
				#print u'Другие условия=', x6
				print u'Пол=', x7
				print u'Возраст=', x8
				print u'Образование=', x9
				print u'Стаж=', x10
				#print u'Другие требования=', x11
				print u'Регион=', x12
				print u'Название=', x13
				print u'Телефон=', x14
				print u'E-mail=', x15
				print u'Адрес сайта=', x16
				print u'Адрес=', x17
				print u'Ссылка=', x18
				
				print u'-------------------------'
			
		if next_url:
			if DEBUG: print 'next_url=', next_url
			
			item_parser_r(next_url, deep+1)
			
	item_parser_r(HREF_START, 1)
	
	file_name = u'rabotavtomske_ru_%s.xls' % datetime.datetime.now().strftime('%d%m%y%H%M%S')
	if DEBUG: print file_name

	title = [
		u'Заголовок',
		u'Категория вакансии',
		u'Дата', 
		u'Заработная плата', 
		u'График работы', 
		u'Другие условия', 
		u'Пол', 
		u'Возраст', 
		u'Образование', 
		u'Стаж', 
		u'Другие требования',
		u'Регион',
		u'Название',
		u'Телефон',
		u'E-mail',
		u'Адрес сайта',
		u'Адрес',
		u'Ссылка',
	]
	p.save(title, file_name)
	
	return 1
	
######################################################################################################################
######################################################################################################################

if __name__ == "__main__":
	u'''
		http://rabotavtomske.ru
		rabotavtomske_ru.py [count]
		count - Необязательный параметр. Количество страниц, которое требуется обработать.
		Если count = 0 или не указан, то будут обработаны все страницы.
	'''
	
	pages_count = None
	
	if len(sys.argv) == 2: pages_count = int(sys.argv[1])
	
	Parser(pages_count)
	
######################################################################################################################
######################################################################################################################