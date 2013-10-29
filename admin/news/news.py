from django.shortcuts import render_to_response
from admin.forms import NewsForm
from oj.models import News
from admin.is_login.is_login import *
from oj.qduoj_config.qduoj_config import *
from admin.admin_backends import is_manager

@is_manager
def news_sc(req, context):
    news = News.objects.order_by('-time')
    if len(news) > 100:
        news = news[0:100]
    return render_to_response('admin_news.html', {
        'news':news}
    )

@is_manager
def add_news_sc(req, context):
    if req.method == 'POST':
        form = NewsForm(req.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(
                '/admin/news_list'
                )
    else:
        form = NewsForm()
    return render_to_response('admin_add_news.html', {
        'context':context, 
        'form':form}
    )

@is_manager
def edit_news_sc(req, context, msgid):
    news = News.objects.filter(id=msgid)
    if len(news) == 0:  #make it true
        pageInfo = 'no this news'
        return render_to_response('error.html' ,{
            'context':context, 
            'pageInfo': pageInfo}
        )
    if req.method == 'POST':
        form = NewsForm(req.POST, instance = news[0])
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/admin/news_list')
    else:
        form = NewsForm(instance = news[0])
    return render_to_response('admin_edit_news.html', {
        'context':context, 
        'form':form, 
        'news':news[0]}
    )

@is_manager
def news_visible_sc(req, context, msgid):
    new = News.objects.filter(id=msgid)
    if len(new) == 0:  #make it true
        pageInfo = 'no this news!'
        return render_to_response('error.html',{
            'context':context,
            'pageInfo':pageInfo}
        )
    if new[0].visible == True:
        new.update(visible=False)
    else:
        new.update(visible=True)
    return HttpResponseRedirect(
        '/admin/news_list'
        )
