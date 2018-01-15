# -*- coding: utf-8 -*-

import re

from annoying.functions import get_object_or_None

################################################################################################################
################################################################################################################

# CHOICE = [
	# ( pk, [u'pattern 1', ...] )
# ]

def get_attr_fk(model, choice, s, errors_item=u'', list_num=1):
	'''
		Находит pk записи в модели model, для которой найденно совподение s с паттерном, и возвращает объект или None.
	'''
	tmp = None
	if s:
		for i in choice:
			for j in i[list_num]:
				if j:
					if re.search(j.strip(), s.strip(), flags=re.I):
						tmp = get_object_or_None(model, pk=i[0])
						break
		if not tmp:
			errors_item += u'Не найден(а) "%s" в "%s"\n' % (s, model._meta.verbose_name)

	return [tmp, errors_item]

################################################################################################################
################################################################################################################