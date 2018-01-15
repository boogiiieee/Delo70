# -*- coding: utf-8 -*-

from django.contrib import admin
from django.conf import settings

from simpleblocks.models import Block

##########################################################################
##########################################################################

class BlockAdmin(admin.ModelAdmin):
	list_display = ('title', 'ident', 'location')
	list_filter = ('location',)
	
	# def has_add_permission(self, *args, **kwargs):
		# if not settings.DEBUG: return False
		# return super(BlockAdmin, self).has_add_permission(*args, **kwargs)
		
	# def has_delete_permission(self, *args, **kwargs):
		# if not settings.DEBUG: return False
		# return super(BlockAdmin, self).has_delete_permission(*args, **kwargs)
 
admin.site.register(Block, BlockAdmin)

##########################################################################
##########################################################################