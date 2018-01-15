# -*- coding: utf-8 -*-

from django.template.base import Node, NodeList, Template, Context, Variable
from django import template

register = template.Library()

################################################################################################################
################################################################################################################

@register.filter(name='count_vacation_location')
def count_vacation_location(category, location):
	return category.get_count_vacancy(location=location)
	
@register.filter(name='count_resume_location')
def count_resume_location(category, location):
	return category.get_count_resume(location=location)

################################################################################################################
################################################################################################################

################################################################################################################
################################################################################################################

@register.filter(name='get_category_vacancy_absolut_url')
def get_category_vacancy_absolut_url(category, location):
	return category.get_absolute_vacancy_url(location=location)
	
@register.filter(name='get_category_resume_absolut_url')
def get_category_resume_absolut_url(category, location):
	return category.get_absolute_resume_url(location=location)

################################################################################################################
################################################################################################################

@register.filter(name='div2')
def div2(mas):
	l = len(mas)/2.0
	i = int(l)
	if i<l: i = i+1
	return i
	
@register.filter(name='mas_2')
def mas_2(mas):
	c = len(mas)
	if c%2==0:
		count = c/2
	else:
		count = c/2+1
	return [mas[:count],mas[count:]]