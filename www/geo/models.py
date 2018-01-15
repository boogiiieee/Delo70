# -*- coding: utf-8 -*-

from django.db import models

from django_geoip.models import City, GeoLocationFacade

##########################################################################
##########################################################################

class CustomLocation(GeoLocationFacade):
	name = models.CharField(max_length=100, verbose_name=u'название')
	slug = models.SlugField(max_length=100, verbose_name=u'псевдоним', unique=True)
	city = models.OneToOneField(City, verbose_name=u'город', related_name='custom_city_location')
	is_default = models.BooleanField(default=False, verbose_name=u'по умолчанию')
	
	def __unicode__(cls):
		return cls.name

	@classmethod
	def get_by_ip_range(cls, ip_range):
		""" Получаем модель географии по IP-дапазону.
		В данном примере диапазон связан с регионом, тот, в свою очередь,  
		связан с нашей кастомной моделью географии
		"""
		if ip_range and ip_range.city:
			return ip_range.city.custom_city_location
		else:
			return cls.get_default_location()

	@classmethod
	def get_default_location(cls):
		""" Локация по-умолчанию, на случай, если не смогли определить местоположение по IP"""
		return cls.objects.get(is_default=True)

	@classmethod
	def get_available_locations(cls):
		return cls.objects.all()

	class Meta:
		db_table = 'geo_location'
		verbose_name = u'город' 
		verbose_name_plural = u'города'
		ordering = ['name']

##########################################################################
##########################################################################
