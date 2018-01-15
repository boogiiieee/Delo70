# -*- coding: utf-8 -*-

from django.contrib import admin

from geo.models import CustomLocation

##########################################################################
##########################################################################
	
class CustomLocationAdmin(admin.ModelAdmin):
	list_display = ('name', 'slug', 'is_default')
	list_filter = ('is_default',)
	prepopulated_fields = {'slug':('name',),}
	
admin.site.register(CustomLocation, CustomLocationAdmin)

##########################################################################
##########################################################################