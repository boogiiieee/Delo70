from django.conf.urls.defaults import *

urlpatterns = patterns('news.views',
	url(r'^$', 'all', name='news_url'),	
	url(r'^(?P<slug>[-_\w]+)/$', 'full', name='news_item_url'),
)