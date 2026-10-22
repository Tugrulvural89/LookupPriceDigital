# myapp/sitemaps.py

from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Post, StaticPages


class PostsSitemap(Sitemap):
    protocol = "https"
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Post.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated


class PagesSitemap(Sitemap):
    protocol = "https"
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return StaticPages.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated


class StaticViewSitemap(Sitemap):
    protocol = "https"
    changefreq = "monthly"
    priority = 0.9

    def items(self):
        return ['index', 'index_es', 'index_tr', 'blog']

    def location(self, item):
        return reverse(item)

