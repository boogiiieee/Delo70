# -*- coding: utf-8 -*-
from django.utils.html import escape
from django.contrib import admin

from complaint.models import Complaints

class ComplaintsAdmin(admin.ModelAdmin):
	list_display = ('get_text', 'get_url', 'is_done', )
	readonly_fields = ('get_url', )
	ordering = ('is_done', '-created')
	list_editable = ['is_done', ]

	def get_url(self, obj): return u'<a href="%s" target="_blanck">%s</a>' % (obj.url, obj.url)
	get_url.short_description = u'Ссылка'
	get_url.allow_tags = True

	def get_text(self, obj): return escape(obj.text)
	get_text.short_description = u'Текст'
	get_text.allow_tags = True


admin.site.register(Complaints, ComplaintsAdmin)