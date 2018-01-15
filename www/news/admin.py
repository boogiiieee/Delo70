# -*- coding: utf-8 -*-

from django.contrib import admin

from sorl.thumbnail.admin import AdminImageMixin

from news.models import NewsArticle

##########################################################################
##########################################################################

class NewsArticleAdmin(AdminImageMixin, admin.ModelAdmin):
	list_display = ('title', 'slug', 'created_at', 'is_active', 'sort')
	list_filter = ('is_active', 'created_at')
	list_editable = ('is_active', 'sort')
	prepopulated_fields = {"slug": ("title",),} 
	fieldsets = (
		(None, {'fields': ('title', 'slug', 'image', 'announcement', 'text', 'is_active', 'sort')},),
		(u'Мета-теги', {'classes': ('collapse',), 'fields': ('description', 'keywords')}),
	)
	
admin.site.register(NewsArticle, NewsArticleAdmin)

##########################################################################
##########################################################################