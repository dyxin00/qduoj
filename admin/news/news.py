from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.paginator import Paginator
from oj.forms import *
from oj.models import *
from admin.is_login.is_login import *
from oj.qduoj_config.qduoj_config import *

def news_sc(req, context):
	is_ok = is_manager_login(req, context)
	if is_ok == 0:
		return HttpResponseRedirect('/admin/admin_login')
	news = News.objects.order_by('-time')
	if len(news) > 100:
		news = news[0:100]
	return render_to_response('admin_news.html', {'news':news})

def add_news_sc(req, context):
	is_ok = is_manager_login(req, context)
	if is_ok == 0:
		return HttpResponseRedirect('/admin/admin_login')
	if req.method == 'POST':
		form = admin_news(req.POST)
		if form.is_valid():
			title = form.cleaned_data['title']
			content = form.cleaned_data['content']
			news = News.objects.create(title=title, content=content)
			news.save()
			return HttpResponseRedirect('/admin/news_list')
	else:
		form = admin_news()
	return render_to_response('admin_add_news.html', {'context':context, 'form':form})

def edit_news_sc(req, msgid, context):
	news_info = {}
	news = News.objects.filter(id=msgid)
	if len(news) == 0:  #make it true
		pageInfo = 'no this news'
		return render_to_response('error.html' ,{'context':context, 'pageInfo': pageInfo})
	is_ok = is_manager_login(req, context)
	if is_ok == 0:
		return HttpResponseRedirect('/admin/admin_login')
	if req.method == 'POST':
		form = admin_news(req.POST)
		if form.is_valid():
			title = form.cleaned_data['title']
			content = form.cleaned_data['content']
				
			news.update(title=title, content=content)
			return HttpResponseRedirect('/admin/news_list')
	else:
		news_info['title'] = news[0].title
		news_info['content'] = news[0].content

		form = admin_news(news_info)
	return render_to_response('admin_edit_news.html', {'context':context, 'form':form, 'news':news[0]})

def news_visible_sc(req, msgid, context):
	new = News.objects.filter(id=msgid)
	if len(new) == 0:  #make it true
		pageInfo = 'no this news!'
		return render_to_response('error.html',{'context':context, 'pageInfo':pageInfo})
	is_ok = is_manager_login(req, context)
	if is_ok == 0:
		return HttpResponseRedirect('/admin/admin_login')
	if new[0].visible == True:
		new.update(visible=False)
	else:
		new.update(visible=True)
	return HttpResponseRedirect('/admin/news_list')
