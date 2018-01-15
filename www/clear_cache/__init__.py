# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
from django.db import connection
from django.conf import settings

_('Clear_Cache')

def clearcache():
	cursor = connection.cursor()
	cursor.execute('DELETE FROM %s' % settings.CACHE_TABLE)
	cursor.execute("COMMIT")