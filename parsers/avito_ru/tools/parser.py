# -*- coding: utf-8 -*-

import re

import xlwt

######################################################################################################################
######################################################################################################################

class Item():
	def __init__(self, *args):
		self.args = args
		
class Price():
	def __init__(self):
		self.items = []
		
	def add(self, *args, **kwargs):
		self.items.append( Item(*args, **kwargs) )
		
	def save(self, title, file_name):
		font0 = xlwt.Font()
		font0.name = 'Times New Roman'
		font0.bold = True
		
		font1 = xlwt.Font()
		font1.name = 'Times New Roman'
		
		style0 = xlwt.XFStyle()
		style0.font = font0
		
		style1 = xlwt.XFStyle()
		style1.font = font1

		wb = xlwt.Workbook()
		ws = wb.add_sheet('vacancy tomsk ru')

		for i in range(len(title)):
			ws.write(0, i, title[i], style0)
				
		for i in range(len(self.items)):
			for j in range(len(self.items[i].args)):
				ws.write(1 + i, j, self.items[i].args[j], style1)

		wb.save(file_name)
		
######################################################################################################################
######################################################################################################################

def find_email(s):
	tmp = re.findall(ur'[0-9a-zA-Z-_]+?@[0-9a-zA-Z-_]+?\.[0-9a-zA-Z-_]{1,9}', s)
	if tmp:
		return tmp
	return []

def find_phone(s):
	if s:
		tmp2 = []
		tmp = re.findall(ur'[\d+\-\(\) ]{6,20}', s)
		for i in tmp:
			tmp1 = re.sub(ur'[^\d]', u'', i)
			if len(tmp1) in [11, 10, 6, 9]:
				tmp2.append(tmp1)
		if tmp2:
			return tmp2
	return []
					
######################################################################################################################
######################################################################################################################

def clean_str(x):
	p = re.compile('^\s+|\n|\r|\s+$')
	return p.sub('', x)
	
######################################################################################################################
######################################################################################################################