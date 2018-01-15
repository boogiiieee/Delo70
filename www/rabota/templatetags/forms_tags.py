# -*- coding: utf-8 -*-

from django.template.base import Node, NodeList, Template, Context, Variable
from django import template
from django import forms
import re

register = template.Library()

################################################################################################################
################################################################################################################

@register.filter(name='has_elm')
def has_elm(var, elm):
	if type(var) is tuple and elm in var: return True
	return False

################################################################################################################
################################################################################################################

@register.filter(name='is_tuple')
def is_tuple(var):
	if type(var) is tuple: return True
	return False

################################################################################################################
################################################################################################################

@register.filter(name='form_filed')
def form_filed(form, field_name):
	if field_name in form.fields.keys():
		boundField = forms.forms.BoundField(form, form.fields[field_name], field_name)
		return boundField
	return u''
	
@register.filter(name='has_visible_fields')
def has_visible_fields(form, row):
	''' Содержит ли form видимые поля строки из fieldset '''
	visible_fields = [i.name for i in form.visible_fields()]

	if type(row) is tuple:
		for i in row:
			if i in visible_fields:
				return True
	else:
		if row in visible_fields:
			return True
	return False	

################################################################################################################
################################################################################################################