# -*- coding: utf-8 -*-

from django import forms
from configuration.models import ConfigModel

class ConfigForm(forms.ModelForm):
	class Meta:
		model = ConfigModel