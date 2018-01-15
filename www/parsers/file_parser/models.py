# -*- coding: utf-8 -*-

from django.db import models
import re, os

from pytils.translit import slugify

from geo.models import CustomLocation

################################################################################################################
################################################################################################################

#Загрузчик
class Uploader(models.Model):
	title = models.CharField(max_length=500, verbose_name=u'название')
	callback = models.CharField(max_length=500, verbose_name=u'функция', help_text=u'parsers.file_parser.callbacks.file_callback')
	sort = models.IntegerField(verbose_name=u'порядок', default=0)
	
	def __unicode__(self):
		return self.title
			
	class Meta: 
		verbose_name = u'загрузчик'
		verbose_name_plural = u'загрузчики'
		ordering = ['sort', '-id']
		
################################################################################################################
################################################################################################################

STATUS = (
	('0', u'В очереди'),
	('1', u'В работе'),
	('2', u'Загружен'),
	('3', u'Загружен с ошибкой'),
)
		
#Файл
class File(models.Model):
	def make_upload_path(instance, filename):
		name, extension = os.path.splitext(filename)
		filename = u'%s%s' % (slugify(name), extension)
		return u'upload/parsers/file_parser/%s' % filename.lower()
		
	uploader = models.ForeignKey(Uploader, verbose_name=u'загрузчик')
	file = models.FileField(max_length=500, upload_to=make_upload_path, verbose_name=u'файл')
	city = models.ForeignKey(CustomLocation, verbose_name=u'город')
	status = models.CharField(max_length=10, choices=STATUS, default='0', verbose_name=u'статус')
	
	errors = models.TextField(max_length=100000, verbose_name=u'сообщения', blank=True)
	
	count_item = models.IntegerField(default=0, verbose_name=u'загружено позиций')
	
	date_creat = models.DateTimeField(verbose_name=u'дата создания', auto_now_add=True)
	date_start = models.DateTimeField(verbose_name=u'дата запуска', blank=True, null=True)
	date_end = models.DateTimeField(verbose_name=u'дата завершения', blank=True, null=True)
	
	def __unicode__(self):
		return u'#%d' % self.id
		
	def is_last(self):
		try:
			obj = File.objects.latest('id')
		except:
			return False
		else:
			return True if obj.id == self.id else False
		
	class Meta: 
		verbose_name = u'файл'
		verbose_name_plural = u'файлы'
		ordering = ['-id']

################################################################################################################
################################################################################################################