# -*- coding: utf-8 -*-

from django.db import models
import datetime


###########################################################################################
###########################################################################################

class OldComplaintsManager(models.Manager): 
	def get_query_set(self): 
		time_ago = datetime.datetime.now() - datetime.timedelta(days=7)
		return super(OldComplaintsManager, self).get_query_set().filter(modified__lte=time_ago)

class Complaints(models.Model): 
	url = models.URLField(verbose_name=u'ссылка', help_text=u'ссылка на жалобу пользователя', max_length=200)
	text = models.TextField(verbose_name=u'жалоба', help_text=u'текст жалобы', max_length=200)
	is_done = models.BooleanField(verbose_name=u'обработано', default=False)	

	created = models.DateTimeField(verbose_name=u'дата создания', default=datetime.datetime.now()) 
	modified = models.DateTimeField(verbose_name=u'дата обновления', auto_now=True)	

	def __unicode__(self):
		return u'Жалоба № %d' % self.id

	objects = models.Manager()
	old_complaints = OldComplaintsManager()

	class Meta:
		verbose_name = u'жалоба'
		verbose_name_plural = u'жалобы'
		ordering = ('is_done', '-created')

############################################################################################
############################################################################################

