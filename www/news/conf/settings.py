# -*- coding: utf-8 -*-

import os
from django.conf import settings

PAGINATE_BY = getattr(settings, 'PAGINATE_BY', 3)