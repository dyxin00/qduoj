from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from oj.forms import *
from oj.models import *
from is_login import *

def news_sc(req, context):
	is_ok = is_manager_login(req, context)
	if is_ok == 0:
		return HttpResponseRedirect('/admin/admin_login')
	news = News.objects.order_by('-time')
	if len(news) > 100:
		news = news[0:100]
	return render_to_response('admin_news.html')
