# -*- coding: utf-8 -*-

from django.contrib import admin

from configuration.models import ConfigModel
from configuration.forms import ConfigForm

##########################################################################
##########################################################################

class ConfigModelAdmin(admin.ModelAdmin):
	form = ConfigForm
	fieldsets = (
		(None, {'fields': ('is_active',)}),
		(None, {'fields': ('clear_cache_link',)}),
	)
	readonly_fields = ('clear_cache_link',)
	
	def clear_cache_link(self, obj):
		return u'<a href="/cache/clear_cache/">очистить</a>'
	clear_cache_link.short_description = u'Очистить кэш'
	clear_cache_link.allow_tags = True
	
	def has_add_permission(self, *args, **kwargs):
		return False
		
	def has_delete_permission(self, *args, **kwargs):
		return False
	
admin.site.register(ConfigModel, ConfigModelAdmin)

##########################################################################
##########################################################################