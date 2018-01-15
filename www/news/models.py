# -*- coding: utf-8 -*-

from django.db import models
import datetime
import re, os

from pytils.translit import slugify
from redactor.fields import RedactorField
from sorl.thumbnail import ImageField as SorlImageField

##########################################################################
##########################################################################

class NewsArticle(models.Model):
	def make_upload_path(instance, filename):
		name, extension = os.path.splitext(filename)
		filename = u'%s%s' % (slugify(name), extension)
		return u'upload/news/%s' % filename.lower()
		
	title = models.CharField(max_length=100, verbose_name=u'заголовок')
	image = SorlImageField(upload_to=make_upload_path, verbose_name=u'изображение', blank=True, null=True)
	announcement = models.TextField(max_length=500, verbose_name=u'анонс')
	text = RedactorField(max_length=100000, verbose_name=u'текст')
	slug = models.SlugField(max_length=500, verbose_name=u'псевдоним', unique=True)
	created_at = models.DateTimeField(verbose_name=u'дата создания', auto_now_add=True)
	is_active = models.BooleanField(verbose_name=u'активно', default=True)
	sort = models.IntegerField(verbose_name=u'порядок', default=0)
	
	description = models.TextField(u'описание', blank=True)
	keywords = models.TextField(u'ключевые слова через запятую', blank=True)
	
	def get_title(self): return self.title
	def get_image(self): return self.image
	def get_announcement(self): return self.announcement
	def get_text(self): return self.text
	def get_created_at(self): return self.created_at
	
	def __unicode__(self):
		return u'%s' % self.get_title()
		
	@models.permalink
	def get_absolute_url(self):
		return ('news_url', (), {})
		
	@models.permalink
	def get_item_url(self):
		return ('news_item_url', (), {'slug':self.slug})
		
	def get_admin_url(self):
		return u'/admin/news/newsarticle/%d/' % self.id
		
	class Meta: 
		verbose_name = u'новость'
		verbose_name_plural = u'новости'
		ordering = ['sort', '-created_at']
		
##########################################################################
##########################################################################