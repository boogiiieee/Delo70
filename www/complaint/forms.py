# -*- coding: utf-8 -*-

from django import forms

#Форма отправки сообщения об ошибке в объявлении/резюме 

class ComplaintForm(forms.Form):
	message = forms.CharField( max_length=200, widget=forms.Textarea(attrs={'required':True, 'class':'span12', 'rows' : '5', 'cols' : '30'}), label="Сообщение")