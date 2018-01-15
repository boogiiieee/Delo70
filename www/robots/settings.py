from django.conf import settings

SITEMAP_URLS = []
SITEMAP_URLS.extend(getattr(settings, 'ROBOTS_SITEMAP_URLS', []))
SITEMAP_HOST = getattr(settings, 'ROBOTS_SITEMAP_HOST', False)
USE_SITEMAP = getattr(settings, 'ROBOTS_USE_SITEMAP', True)
CACHE_TIMEOUT = getattr(settings, 'ROBOTS_CACHE_TIMEOUT', None)