from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Page

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['index', 'about']

    def location(self, item):
        return reverse(item)

class PageSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Page.objects.all()

    def lastmod(self, obj):
        return obj.last_update

    def location(self, obj):
        return f'/courses/{obj.category}/{obj.slug}/'
