# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.models import User, AnonymousUser
from django.forms.widgets import TextInput
from django.forms.extras import SelectDateWidget
import datetime

from registration.forms import RegistrationForm
from django.contrib.auth.forms import PasswordResetForm
from captcha.fields import CaptchaField

from rabota.models import Category, Vacancy, Resume, SubscribeVacancy, SubscribeResume
from rabota.widgets import ImageWidget

##################################################################################################	
##################################################################################################

##################################################################################################	
##################################################################################################

TYPE_SEARCH = [
	(u'vacancy', u'Вакансии'),
	(u'resume', u'Резюме'),
]

class SearchMinForm(forms.Form):
	q = forms.CharField(max_length=50, label=u'Ключевое слово, фраза', required=False, widget=TextInput(attrs={'placeholder':u'Ключевое слово, фраза','class':'span11'}))
	category = forms.ModelMultipleChoiceField(queryset=Category.activs.all(), label=u'Раздел', required=False)
	type_search = forms.ChoiceField(choices=TYPE_SEARCH, widget=forms.RadioSelect(attrs={'required':True}), label=u'', required=True)
	
	def __init__(self, type_search=TYPE_SEARCH[0][0], *args, **kwargs):
		super(SearchMinForm, self).__init__(*args, **kwargs)
		self.fields['type_search'].initial = type_search

##################################################################################################	
##################################################################################################

SearchVacancyFieldsets = (
	(None, {
		'fields': (('q', 'category',), ('schedule', 'type_employment'), ('wage_min', 'wage_max', 'type_wages'), ('education', 'experience',), ('city',))
	}),
)

class SearchVacancyForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(SearchVacancyForm, self).__init__(*args, **kwargs)
		self.fields['category'].queryset = Category.activs.all()
		self.fields['category'].help_text = None
		for key in self.fields:
			self.fields[key].required = False
		self.fieldsets = SearchVacancyFieldsets
			
	q = forms.CharField(max_length=50, label=u'Ключевое слово, фраза', required=False)
	
	class Meta:
		model = Vacancy
		fields = (
			'q', 'category',
			'schedule', 'type_employment', 'wage_min', 'wage_max', 'type_wages',
			'education', 'experience',
			'city',
		)

##################################################################################################	
##################################################################################################

SearchResumeFieldsets = (
	(None, {
		'fields': (('q', 'category',), ('wage_min', 'type_wages', 'schedule', 'type_employment'), ('education', 'experience'), ('city',))
	}),
)
		
class SearchResumeForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(SearchResumeForm, self).__init__(*args, **kwargs)
		self.fields['category'].queryset = Category.activs.all()
		self.fields['category'].help_text = None
		for key in self.fields:
			self.fields[key].required = False
		self.fieldsets = SearchResumeFieldsets
			
	q = forms.CharField(max_length=50, label=u'Ключевое слово, фраза', required=False)
	
	class Meta:
		model = Resume
		fields = (
			'q', 'category',
			'schedule', 'type_employment', 'wage_min', 'type_wages',
			'experience', 'education',
			'city',
		)

##################################################################################################	
##################################################################################################

##################################################################################################	
##################################################################################################

AddVacancyFieldsets = (
	(u'Основная информация', {
		'fields': (('post', 'category',),)
	}),
	(u'Описание вакансии', {
		'fields': (('schedule', 'type_employment'), ('wage_min', 'wage_max', 'type_wages'), 'brief', 'description',)
	}),
	(u'Требования к соискателю', {
		'fields': (('education', 'experience'), 'professional_skills',)
	}),
	(u'Контактная информация', {
		'fields': (('company', 'fio', 'site', 'logo'), ('phone1', 'other_phone1', 'phone2', 'other_phone2'), ('email', 'icq', 'skype'), ('city', 'street', 'home', 'other_address',),)
	}),
)
		
class AddVacancyForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(AddVacancyForm, self).__init__(*args, **kwargs)
		self.fields['category'].queryset = Category.activs.all()
		self.fields['category'].help_text = None
		self.fieldsets = AddVacancyFieldsets
		
	class Meta:
		model = Vacancy
		fields = (
			'post', 'brief', 'category',
			'schedule', 'type_employment', 'wage_min', 'wage_max', 'type_wages', 'description',
			'education', 'experience', 'professional_skills',
			'company', 'fio', 'phone1', 'other_phone1', 'phone2', 'other_phone2', 'email', 'icq', 'skype', 'site', 'city', 'street', 'home', 'other_address', 'logo',
		)
		widgets = {
			'logo': ImageWidget(attrs={}),
			'description':forms.Textarea(attrs={'class':'span12', 'rows':3}),
			'professional_skills':forms.Textarea(attrs={'class':'span12', 'rows':3}),
			'brief':forms.TextInput(attrs={'class':'span12', 'rows':3}),
		}
		
##################################################################################################	
##################################################################################################

AddResumeFieldsets = (
	(u'Основная информация', {
		'fields': (('post', 'category',),)
	}),
	(u'О будущей работе', {
		'fields': (('wage_min', 'type_wages',), ('schedule', 'type_employment', 'willing_travel') )
	}),
	(u'Опыт/образование', {
		'fields': ('summary', ('experience', 'education', 'educational_institution', 'major_subject', ), 'extras_education', 'professional_skills' )
	}),
	(u'Контактная информация', {
		'fields': (('fio', 'photo', 'dob'), ('phone1', 'other_phone1'), ('email', 'icq', 'skype'), ('city',),)
	}),
	(u'О себе', {
		'fields': (('sex', 'marital_status'), ('driver_license', 'smoke'), 'personal_qualities',)
	}),
)
		
class AddResumeForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(AddResumeForm, self).__init__(*args, **kwargs)
		self.fields['category'].queryset = Category.activs.all()
		self.fields['category'].help_text = None
		self.fieldsets = AddResumeFieldsets
		
	class Meta:
		model = Resume
		fields = (
			'post', 'category',
			'schedule', 'type_employment', 'wage_min', 'type_wages',
			'fio', 'photo', 'dob', 'sex', 'marital_status', 'experience', 'professional_skills', 'education', 'educational_institution', 'major_subject', 'extras_education', 'personal_qualities', 'driver_license', 'willing_travel', 'smoke', 'summary',
			'phone1', 'other_phone1', 'email', 'icq', 'skype', 'city',
		)
		widgets = {
			'photo': ImageWidget(attrs={}),
			'professional_skills':forms.Textarea(attrs={'class':'span12', 'rows':3}),
			'extras_education':forms.Textarea(attrs={'class':'span12', 'rows':3}),
			'personal_qualities':forms.Textarea(attrs={'class':'span12', 'rows':3}),
			'dob': SelectDateWidget(attrs={'class':'span4'}, years=range(1930, datetime.datetime.now().year-14)),
		}
		
		
##################################################################################################	
##################################################################################################

##################################################################################################	
##################################################################################################

AddVacancySubscribeFieldsets = (
	(u'Основная информация', {
		'fields': (('category',), ('schedule', 'type_employment'), ('wage_min', 'wage_max', 'type_wages'), ('city',))
	}),
	(u'Образование/Опыт', {
		'fields': (('education', 'experience',),)
	}),
)

class AddVacancySubscribeForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(AddVacancySubscribeForm, self).__init__(*args, **kwargs)
		self.fields['category'].queryset = Category.activs.all()
		self.fields['category'].help_text = None
		self.fieldsets = AddVacancySubscribeFieldsets
		
	class Meta:
		model = SubscribeVacancy
		fields = (
			'category',
			'schedule', 'type_employment', 'wage_min', 'wage_max', 'type_wages', 'city',
			'education', 'experience',
		)

		
##################################################################################################	
##################################################################################################

AddResumeSubscribeFieldsets = (
	(u'Основная информация', {
		'fields': (('category',), ('schedule', 'type_employment'), ('wage_min', 'type_wages'), ('city',))
	}),
	(u'Образование/Опыт', {
		'fields': (('education', 'experience',),)
	}),
)

class AddResumeSubscribeForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(AddResumeSubscribeForm, self).__init__(*args, **kwargs)
		self.fields['category'].queryset = Category.activs.all()
		self.fields['category'].help_text = None
		self.fieldsets = AddResumeSubscribeFieldsets
		
	class Meta:
		model = SubscribeResume
		fields = (
			'category',
			'schedule', 'type_employment', 'wage_min', 'type_wages', 'city',
			'experience', 'education',
		)

##################################################################################################	
##################################################################################################

##################################################################################################	
##################################################################################################

#Профиль пользователя
class ProfileForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'email')

#Форма регистрации		
class RegistrationCaptchaForm(RegistrationForm):
	def __init__(self, *args, **kwargs):
		super(RegistrationCaptchaForm, self).__init__(*args, **kwargs)
		self.fields['username'].label = u'Логин'
		
	captcha = CaptchaField(label=u'Код защиты')
	
#Форма восстановления пароля
class PasswordResetCaptchaForm(PasswordResetForm):
	captcha = CaptchaField(label=u'Код защиты')
		
##################################################################################################	
##################################################################################################

##################################################################################################	
##################################################################################################