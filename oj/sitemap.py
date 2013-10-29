# coding=utf-8

from django.contrib.sitemaps import Sitemap
from oj.models import Problem

class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = '0.2'
    
    def items(self):
        return Problem.objects.all()
    
    def lastmod(self, obj):
        return obj.in_date
    
    def location(self, obj):
        return '/problem/num=%s' % obj.problem_id
