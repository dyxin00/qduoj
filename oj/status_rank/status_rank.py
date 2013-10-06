#coding=utf-8

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from oj.models import *
from oj.forms import *

#有定时刷新
def rank_sc(req, page, context):
	list_info = {}
	page_num = []
	page = int(page)
	users = User.objects.order_by('-ac','submit')
	user_len = len(users)
	for i in range(0, 15):
		page_num.append(i + 1)
	list_info['len'] = page_num
	list_info['page'] = page
	if page > 15 or (page - 1) * 30 > user_len:
		pageInfo = 'page not found maybe you are far behind!'
		title = '404 not found'
		return render_to_response('error.html', {'pageInfo':pageInfo, 'title':title, 'context':context})	
	users = users[30 * (page - 1):30 * page - 1]
	return render_to_response('user_rank.html', {'users':users, 'context':context, 'list_info':list_info})
	
	
