# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url
from django.contrib.sitemaps import FlatPageSitemap, GenericSitemap
from django.contrib.sitemaps.views import index, sitemap
from django.views.decorators.cache import cache_page
from django.contrib.auth import views as auth_views
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

from rabota.views import RegistrationCaptchView
from rabota.forms import PasswordResetCaptchaForm
from rabota.sitemap import VacancyItemSitemap, ResumeItemSitemap
from news.views import NewsSitemap

sitemaps = {
	'flatpages': FlatPageSitemap, #Главная и контакты
	'vacancy_item': VacancyItemSitemap, #Вакансии. Подробно
	'resume_item': ResumeItemSitemap, #Резюме. Подробно
	'news': NewsSitemap, # Новости 
}

urlpatterns = patterns('',
	url(r'^accounts/password/reset/$', 'django.contrib.auth.views.password_reset', {'password_reset_form':PasswordResetCaptchaForm, 'template_name':'registration/password_reset_form1.html', 'email_template_name':'registration/password_reset_email1.html'} ),
	url(r'^accounts/password/reset/done/$', 'django.contrib.auth.views.password_reset_done', {'template_name':'registration/password_reset_done1.html',} ),
	url(r'^accounts/password/reset/confirm/(?P<uidb36>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', 'django.contrib.auth.views.password_reset_confirm', {'template_name':'registration/password_reset_confirm1.html',} ),
	url(r'^accounts/password/reset/complete/$', 'django.contrib.auth.views.password_reset_complete', {'template_name':'registration/password_reset_complete1.html',} ),
	url(r'^accounts/logout/$', auth_views.logout, {'next_page': '/'}, name='auth_logout'),
	url(r'^accounts/login/$', auth_views.login),
	url(r'^accounts/register/$', RegistrationCaptchView.as_view(), name='registration_register'),
	url(r'^accounts/', include('registration.backends.simple.urls')),
	
	url(r'^admin_tools/', include('admin_tools.urls')),
	url(r'^admin/', include(admin.site.urls)),
	
	url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
	url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
	
	url(r'^redactor/', include('redactor.urls')),
	url(r'^captcha/', include('captcha.urls')),
	
	url(r'^geoip/', include('django_geoip.urls')),
	
	url(r'^', include('rabota.urls')),
	url(r'^article/', include('news.urls')),
	
	url(r'^cache/', include('clear_cache.urls')),
	
	url(r'^robots\.txt$', include('robots.urls')),
	
	url(r'^sitemap\.xml$', cache_page(60 * 60 * 3)(index), {'sitemaps': sitemaps, 'sitemap_url_name':'sitemaps'}),
	url(r'^sitemap-(?P<section>.+)\.xml$', cache_page(60 * 60 * 3)(sitemap), {'sitemaps': sitemaps}, name='sitemaps'),
	
	url(r'^complaint_text/', include('complaint.urls')),
)

urlpatterns += patterns('ibanners.views',
	url(regex=r'^ibas/(?P<banner_id>\d+)/$',view='banner', name='ibanners.banner'),
	url(regex=r'^zones/(?P<zone_id>\d+)/$', view='zones', name='ibanners.zones'),
	url(regex=r'^zonejs/(?P<zonejs_id>\d+)/$', view='zonejs', name='ibanners.zonejs'),
	url(regex=r'^zonesjs/$', view='zonesjs', name='ibanners.zonesjs'),
)
