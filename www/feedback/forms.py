# -*- coding: utf-8 -*-

from django import forms
from captcha.fields import CaptchaField, CaptchaTextInput
import cgi
import re

from feedback.models import FeedBackItem

################################################################################################################
################################################################################################################
class FeedBackForm(forms.ModelForm):
	captcha = CaptchaField(label=u'Код защиты', widget=CaptchaTextInput(attrs={'placeholder':'Код защиты', 'class':'span8', 'required':True}))
	
	def __init__(self, *args, **kwargs):
		super(FeedBackForm, self).__init__(*args, **kwargs)
	
	class Meta:
		model = FeedBackItem
		fields = ('name', 'email', 'phone', 'captcha', 'msg')
		widgets = {
			'msg':forms.Textarea(attrs={'placeholder':"Сообщение", 'rows':"8", 'class':"span12", 'required':True}), 
			'name': forms.TextInput(attrs={'placeholder':"ФИО", 'class':"span12", 'required':True }),
			'email': forms.TextInput(attrs={'placeholder':"Email", 'class':'span12', 'required':True}),
			'phone': forms.TextInput(attrs={'placeholder':"Телефон", 'class':'span12'})
		}
		
	def clean_name(self): 
		name = self.cleaned_data['name']
		if len(name) < 3:
			raise forms.ValidationError(u'Слишком короткое ФИО')
		return name
		
	def clean_email(self): 
		email = self.cleaned_data['email']
		if email:
			r = re.compile('^[0-9a-zA-Z]+[-\._0-9a-zA-Z]*@[0-9a-zA-Z]+[-\._^0-9a-zA-Z]*[0-9a-zA-Z]+[\.]{1}[a-zA-Z]{2,6}$')
			if not r.findall(email):
				raise forms.ValidationError(u'Некорректный E-mail')
		return email
		
	def clean_phone(self): 
		phone = self.cleaned_data['phone']
		if phone:
			r = re.compile('^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$')
			if not r.findall(phone):
				raise forms.ValidationError(u'Некорректный номер телефона')
		return phone
		
	def clean_msg(self): 
		msg = self.cleaned_data['msg']
		msg = cgi.escape(msg)
		if len(msg) < 10:
			raise forms.ValidationError(u'Слишком короткое сообщение')
		return msg
		
################################################################################################################
################################################################################################################