# -*- coding: utf-8 -*-

from django.db import models

################################################################################################################
################################################################################################################

class FeedBackItem(models.Model):
	name = models.CharField(max_length=100, verbose_name=u'ФИО')
	email = models.CharField(max_length=100, verbose_name=u'e-mail')
	phone = models.CharField(max_length=100, verbose_name=u'телефон', blank=True)
	msg = models.TextField(max_length=1000, verbose_name=u'сообщение')
	created_at = models.DateTimeField(verbose_name=u'дата создания', auto_now_add=True)
	
	def get_name(self): return self.name
	def get_email(self): return self.email
	def get_phone(self): return self.phone
	def get_msg(self): return self.msg
	def get_created_at(self): return self.created_at
	
	def __unicode__(self):
		return u'%s' % self.get_name()
		
	class Meta: 
		verbose_name = u'сообщение' 
		verbose_name_plural = u'сообщения обратной связи'
		ordering = ['-created_at']
		
################################################################################################################
################################################################################################################