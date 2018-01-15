# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.utils.encoding import force_unicode
from django.utils.html import escape
from django.contrib.admin.util import unquote

from sorl.thumbnail.admin import AdminImageMixin

from rabota.models import Schedule, TypeEmployment, TypeWages, Education, Experience, Category, Vacancy, Resume, SubscribeVacancy, SubscribeResume

##########################################################################
##########################################################################

UserAdmin.list_display += ('phone',)
UserAdmin.fieldsets[1][1]['fields'] += ('phone',)
	
##########################################################################
##########################################################################

class DefaultAdmin(admin.ModelAdmin):
	list_display = ('title', 'is_active', 'order')
	list_filter = ('is_active',)
	list_editable = ('is_active', 'order')

admin.site.register(Schedule, DefaultAdmin)
admin.site.register(TypeEmployment, DefaultAdmin)
admin.site.register(TypeWages, DefaultAdmin)
admin.site.register(Education, DefaultAdmin)
admin.site.register(Experience, DefaultAdmin)

##########################################################################
##########################################################################
	
class CategoryAdmin(admin.ModelAdmin):
	list_display = ('title', 'slug', 'is_active', 'order')
	list_filter = ('is_active',)
	search_fields = ('title',)
	list_editable = ('slug', 'is_active', 'order')
	
admin.site.register(Category, CategoryAdmin)

##########################################################################
##########################################################################

class VacancyAdmin(AdminImageMixin, admin.ModelAdmin):
	list_display = ('post', 'slug', 'brief', 'user', 'created', 'modified', 'stick_date', 'is_active', 'in_archive', 'order')
	list_filter = ('is_active', 'city', 'created', 'modified', 'stick_date', 'in_archive', 'category')
	search_fields = ('user__username', 'user__first_name', 'user__last_name', 'user__email', 'post', 'company', 'fio', 'phone1', 'phone2', 'email', 'icq', 'skype', 'site', 'street')
	filter_horizontal = ('category',)
	list_editable = ('is_active', 'slug', 'in_archive', 'order')
	raw_id_fields = ('user',) 
	
	fieldsets = (
		(None, {'fields':('user', 'order', 'in_archive', 'is_active')}),
		(u'Общая информация о вакансии', {'classes':('extrapretty',), 'fields':('post', 'brief', 'category')}),
		(u'Условия работы', {'classes':('extrapretty',), 'fields':('schedule', 'type_employment', ('wage_min', 'wage_max', 'type_wages'), 'description')}),
		(u'Требования к соискателю', {'classes':('extrapretty',), 'fields':('education', 'experience', 'professional_skills')}),
		(u'Контактная информация', {'classes':('extrapretty',), 'fields':('company', 'fio', ('phone1', 'other_phone1'), ('phone2', 'other_phone2'), 'email', 'icq', 'skype', 'site', ('city', 'street', 'home', 'other_address'), 'logo')}),
		(u'Статистика', {'classes':('extrapretty',), 'fields':('views_count',)}),
		(u'Системные', {'classes':('extrapretty',), 'fields':('stick_date',)}),
	)
	
admin.site.register(Vacancy, VacancyAdmin)

##########################################################################
##########################################################################

class ResumeAdmin(AdminImageMixin, admin.ModelAdmin):
	list_display = ('post', 'slug', 'user', 'created', 'modified', 'is_active', 'in_archive', 'order',)
	list_filter = ('is_active', 'city', 'modified', 'in_archive', 'category',)
	search_fields = ('user__username', 'user__first_name', 'user__last_name', 'user__email', 'user_phone', 'post', 'fio', 'phone1', 'email', 'icq', 'skype',)
	filter_horizontal = ('category',)
	list_editable = ('is_active', 'slug', 'in_archive', 'order',)
	raw_id_fields = ('user',) 
	
	fieldsets = (
		(None, {'fields':('user', 'is_active', 'in_archive')}),
		(u'Требования к должности', {'classes':('extrapretty',), 'fields':('post', 'category', 'schedule', 'type_employment', ('wage_min', 'type_wages'))}),
		(u'Персональные данные', {'classes':('extrapretty',), 'fields':('fio', 'photo', 'dob', 'sex', 'marital_status', 'experience', 'professional_skills', 'education', 'educational_institution', 'major_subject', 'extras_education', 'personal_qualities', ('driver_license', 'willing_travel', 'smoke'), 'summary')}),
		(u'Контактная информация', {'classes':('extrapretty',), 'fields':(('phone1', 'other_phone1'), 'email', 'icq', 'skype', ('city',))}),
		(u'Статистика', {'classes':('extrapretty',), 'fields':('views_count',)}),
	)
	
admin.site.register(Resume, ResumeAdmin)

##########################################################################
##########################################################################

class SubscribeVacancyAdmin(admin.ModelAdmin):	
	list_display = ('user', 'created', 'modified', 'is_active')
	list_filter = ('created', 'modified', 'is_active', 'city')
	search_fields = ('user__username', 'user__first_name', 'user__last_name', 'user__email', 'user_phone',)
	filter_horizontal = ('category',)
	list_editable = ('is_active', )
	
admin.site.register(SubscribeVacancy, SubscribeVacancyAdmin)

##########################################################################
##########################################################################

class SubscribeResumeAdmin(admin.ModelAdmin):	
	list_display = ('user', 'created', 'modified', 'is_active',)
	list_filter = ('created', 'modified', 'is_active', 'city')
	search_fields = ('user__username', 'user__first_name', 'user__last_name', 'user__email', 'user_phone',)
	filter_horizontal = ('category',)
	list_editable = ('is_active',)
	
admin.site.register(SubscribeResume, SubscribeResumeAdmin)

##########################################################################
##########################################################################