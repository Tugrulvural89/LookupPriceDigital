# myapp/sitemaps.py

from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Post, StaticPages


class PostsSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Post.objects.all()

    def lastmod(self, obj):
        return obj.updated


class PagesSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return StaticPages.objects.all()

    def lastmod(self, obj):
        return obj.updated


class StaticViewSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.9

    def items(self):
        return ['index', 'contact', 'blog', 'case', 'search']

    def location(self, item):
        return reverse(item)

