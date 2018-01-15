# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from admin_tools.dashboard import modules, Dashboard, AppIndexDashboard
from admin_tools.utils import get_admin_site_name

class CustomIndexDashboard(Dashboard):

	def init_with_context(self, context):
		site_name = get_admin_site_name(context)
		
		self.children += [
			modules.AppList(
				_('Applications'),
				exclude=('django.contrib.*',),
			),
			modules.AppList(
				_('Administration'),
				models=('django.contrib.*',),
			)
		]


class CustomAppIndexDashboard(AppIndexDashboard):
	title = ''

	def __init__(self, *args, **kwargs):
		AppIndexDashboard.__init__(self, *args, **kwargs)

		self.children += [
			modules.ModelList(_(self.app_title), self.models),
			modules.RecentActions(
				_('Recent Actions'),
				include_list=self.get_app_content_types(),
				limit=5
			)
		]

	def init_with_context(self, context):
		return super(CustomAppIndexDashboard, self).init_with_context(context)