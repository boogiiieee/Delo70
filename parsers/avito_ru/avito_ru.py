# -*- coding: utf-8 -*-

from django.utils.encoding import smart_str
from time import sleep
import re, os, sys, commands
import datetime, random

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

def phoneDemixer(key, item_id):
		u'''Получить pkey номера телефона'''
		p = re.compile(r'[0-9a-f]+')
		pre = p.findall(key)
		
		#print 'pre=', pre
		
		if int(item_id)%2 == 0:
			pre.reverse()

		mixed = pre
		mixed = ''.join(mixed)
		
		#print 'mixed=', mixed
		
		s = len(mixed)
		r = ''
		
		for k in range(0, s):
			if k%3 == 0:
				r += mixed[k]

		return r
		
def get_phone(url, item_url, item_phone):
	u'''
		url = 'http://www.avito.ru/novosibirsk/vakansii/raznorabochie_212424629'
		item_url = 'tomsk_vakansii_raznorabochie_212424629'
		item_phone = '7f2785734a8d4a6o77dae145bba5o21fobd444ec52b259ecc09e909ce152e257e424dff1b5a8b5o91efd7ob6a2d8od43158d2f'
	'''
	
	item_url = item_url.split('_')[-1]
	
	pkey = phoneDemixer(item_phone, item_url)
	
	headers = {
		'Accept':'image/webp,*/*;q=0.8',
		'Accept-Encoding':'gzip,deflate,sdch',
		'Accept-Language':'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4',
		'Connection':'keep-alive',
		'Host':'www.avito.ru',
		'Referer':url,
		'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.76 Safari/537.36',
	}
	
	g1 = Grab(headers=headers)
	g1.setup(hammer_mode=True, hammer_timeouts=((2, 5), (10, 15), (20, 30)))
	# g1.load_proxylist('proxy.txt', 'text_file', proxy_type='http', auto_init=True, auto_change=True)
	g1.go('http://www.avito.ru/items/phone/%s?pkey=%s' % (item_url, pkey))
	g1.response.save('tmp.png')
	
	img = Image.open('tmp.png')
	width, height = img.size
	img_resize = img.resize(((width/height) * (height*2), height*2), Image.BILINEAR)
	img_resize.save('tmp_resize.png')
	
	os.popen("tesseract tmp_resize.png outfile")
	f = open('outfile.txt', 'rb')
	
	res = f.read().strip()
	
	try:
		return unicode(res)
	except:
		return None
		
######################################################################################################################
######################################################################################################################

def Parser(pages_count, city):
	u'''
		Парсер http://www.avito.ru/<Город>/vakansii
	'''
	
	DEBUG = True
	p = Price()
	
	HREF = u'http://www.avito.ru'
	HREF_START = u'http://www.avito.ru/%s/vakansii' % city
	LOG_FILE = u'avito_ru.log'

	g = Grab()
	g.setup(log_file=LOG_FILE, hammer_mode=True, hammer_timeouts=((2, 5), (10, 15), (20, 30)))
	
	def item_parser_r(x, deep):
		if DEBUG:
			print u'deep=', deep
			print u'page=', x
		
		if pages_count and deep > pages_count:
			return
			
		g.go(x)
		
		try: next_url = HREF + g.doc.select(u'//a[@class="next"]/@href')[0].text()
		except: next_url = None
		
		items = g.tree.xpath(u'//*[@class="b-catalog-table"]//h3[@class="title"]/a/@href')
		#items = items[:2]
		
		for item in items:
			sleep( random.randint(5, 10) )
			
			print u'.',
			
			if DEBUG: print u'item=', (HREF + item)
			
			g.go(HREF + item)
					
			try:
				x0 = g.doc.select(u'//h1[contains(@class, "h1")]')[0]
				x0 = clean_str( x0.text().lower().capitalize() )
			except:
				if DEBUG: print u'ERROR: not title' 
			else:
				try:
					x1 = clean_str( g.doc.select(u'//*[contains(@class, "p_i_price")]')[0].text() )
					x1 = re.sub(u'\D', u'', x1) or None
				except:
					x1 = None
					
				try:
					x2 = clean_str( g.doc.select(u'//*[contains(text(), "Контактное лицо:")]')[0].text() )
					x2 = x2.replace(u'Контактное лицо:', u'').strip() or None
				except:
					x2 = None
					
				try:
					x3 = clean_str( g.doc.select(u'//*[@id="seller"]/strong')[0].text() ) or None
				except:
					x3 = None
					
				if g.doc.select(u'//*[contains(text(), "(частное лицо)")]').count():				
					x2, x3 = x3, None
					
				try:
					x4 = clean_str( g.doc.select(u'//*[@id="map"]/a')[0].text() ) or None
				except:
					x4 = None
					
				try:
					x5 = clean_str( g.doc.select(u'//*[contains(@class, "description description-text")]')[0].text() ) or None
				except:
					x5 = None
					
				try:
					tmp = clean_str( g.doc.select(u'//*[contains(@class, "description description-expanded")]//*[contains(@class, "item-params")]')[0].text() ) or None
				except:
					tmp = None
					
				try:
					tmp = re.findall(u'(.*?Сфера деятельности:)(.+?)(График работы:)(.+)', tmp)
				except:
					pass
				
				try:
					x6 = tmp[0][1].strip() or None
				except:
					x6 = None
					
				try:
					x7 = tmp[0][3].strip() or None
				except:
					x7 = None
				
				try:
					item_url = g.rex(re.compile(u"item_url = \'(.+?)\'")).group(1)
					item_phone = g.rex(re.compile(u"item_phone = \'(.+?)\'")).group(1)
				except:
					x8 = None
				else:
					x8 = get_phone(HREF + item, item_url, item_phone) or None
					if x8:
						x8 = x8.replace(u'E', u'8').replace(u'B', u'8')
						x8 = x8.replace(u'O', u'0').replace(u'D', u'0')
						x8 = x8.replace(u'!', u'1').replace(u'I', u'1')
						x8 = x8.replace(u'?', u'2')
						x8 = x8.replace(u'S', u'5')
						x8 = re.sub(u'[^0-9]', u'', x8)
						if not len(x8) in [5,6,7,10,11]:
							x8 = None
				
				p.add(x0, x1, x2, x3, x4, x5, x6, x7, x8, HREF + item)
				
				if DEBUG:
					print u'-------------------------'
					
					print u'Заголовок=', smart_str(x0)
					print u'Зарплата=', smart_str(x1)
					print u'Контактное лицо=', smart_str(x2)
					print u'Название компании=', smart_str(x3)
					print u'Город=', smart_str(x4)
					print u'Текст=', smart_str(x5)
					print u'Сфера деятельности=', smart_str(x6)
					print u'График работы=', smart_str(x7)
					print u'Телефон=', smart_str(x8)
					
					print u'-------------------------'
				
		if next_url:
			if DEBUG: print u'next_url=', next_url
			
			item_parser_r(next_url, deep+1)
			
	item_parser_r(HREF_START, 1)
	
	file_name = u'avito_ru_%s_%s.xls' % (city, datetime.datetime.now().strftime('%d%m%y%H%M%S'))
	if DEBUG: print file_name
		
	title = [
		u'Заголовок',
		u'Зарплата',
		u'Контактное лицо', 
		u'Название компании', 
		u'Город', 
		u'Текст', 
		u'Сфера деятельности', 
		u'График работы', 
		u'Телефон', 
		u'Ссылка',
	]
	p.save(title, file_name)
	
	return 1
	
######################################################################################################################
######################################################################################################################

if __name__ == "__main__":
	u'''
		http://www.avito.ru
		avito_ru.py <count>
		count - Необязательный параметр. Количество страниц, которое требуется обработать.
		Если count = 0 или не указан, то будут обработаны все страницы.
	'''
	
	pages_count = None
	CITY_LIST = [u'strezhevoy', u'omsk', u'novosibirsk', u'krasnoyarsk', u'nizhnevartovsk', u'barnaul', u'kemerovo', u'novokuznetsk']#, u'tomsk']
	
	if len(sys.argv) == 2: pages_count = int(sys.argv[1])
	
	for city in CITY_LIST:
		Parser(pages_count, city)
	
######################################################################################################################
######################################################################################################################