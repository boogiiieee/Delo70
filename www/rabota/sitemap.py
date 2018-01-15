# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.core.paginator import Paginator
from django.contrib.sitemaps import Sitemap
from django.contrib.sites.models import Site
from django.conf import settings

from rabota.models import Category, Vacancy, Resume

##########################################################################
##########################################################################
		
class VacancyItemSitemap(Sitemap):
	changefreq = "monthly"
	priority = 1
	
	def items(self):
		return Vacancy.activs.all()[:2000]
		
	def location(self, obj):
		return obj.get_absolute_url()
		
	def lastmod(self, obj):
		return obj.modified
		
##########################################################################
##########################################################################
		
class ResumeItemSitemap(Sitemap):
	changefreq = "monthly"
	priority = 1
	
	def items(self):
		return Resume.activs.all()[:2000]
		
	def location(self, obj):
		return obj.get_absolute_url()
		
##########################################################################
##########################################################################