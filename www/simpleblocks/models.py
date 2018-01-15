# -*- coding: utf-8 -*-

from django.db import models

from geo.models import CustomLocation

################################################################################################################
################################################################################################################

class Block(models.Model):
	ident = models.CharField(max_length=100, verbose_name=u'идентификатор', help_text=u'Указывается в шаблонном теге.')
	location = models.ForeignKey(CustomLocation, verbose_name=u'город', blank=True, null=True, related_name='custom_location')
	
	title = models.CharField(max_length=200, verbose_name=u'заголовок')
	text = models.TextField(max_length=1000, verbose_name=u'текст')
	
	def get_title(self): return self.title
	def get_text(self): return self.text
	
	def __unicode__(self):
		return self.get_title()
		
	class Meta: 
		verbose_name = u'модуль' 
		verbose_name_plural = u'текстовые модули'
		ordering = ['title']
		
################################################################################################################
################################################################################################################