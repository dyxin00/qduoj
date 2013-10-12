#coding=utf-8
# function: rank, usr_info

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from oj.models import *
from oj.forms import *
from django.core.paginator import Paginator
from qduoj_config import *

def rank_sc(req, page, context):
	list_info = {}
	page_num = []
	try:
		page = int(page)
	except ValueError:
		pageInfo = "page not found"
		title = '404 not found'
		return render_to_response('error.html', {'context':context, 'pageInfo':pageInfo, 'title':title})
	p = Paginator(User.objects.order_by('-ac','submit'), PAGE_RANK_NUM)
	for i in range(0, p.num_pages):
		page_num.append(i + 1)
	list_info['len'] = page_num
	list_info['page'] = page
	if page <=0 or page > 15 or page > p.num_pages:
		pageInfo = 'page not found maybe you are far behind!'
		title = '404 not found'
		return render_to_response('error.html', {'pageInfo':pageInfo, 'title':title, 'context':context})	
	users = p.page(page).object_list
	k = 1
	for user in users:
		User.objects.filter(nick=user.nick).update(rank=(page - 1)*PAGE_RANK_NUM + k)
		k = k + 1
	return render_to_response('user_rank.html', {'users':users, 'context':context, 'list_info':list_info})


def user_info_sc(req, nick, context):
	user = User.objects.filter(nick=nick)
	if len(user) == 0:
		pageInfo = "there is no this user!"
		title = '404 not found!'
		return render_to_response('error.html', {'pageInfo':pageInfo, 'title':title, 'context':context})
	submitions = Solution.objects.filter(user=user[0])
	return render_to_response('user_info.html', {'user':user[0],'context':context})


def source_code_sc(req, runid, context):
	submit = Solution.objects.filter(solution_id=runid)
	if not 'ojlogin' in context or len(submit) == 0:
		pageInfo = "user not login or cant found the submit"
		title = "404 not found"
		return render_to_response('error.html', {'context':context, 'pageInfo':pageInfo, 'title':title})
	user = context['ojlogin'].nick
	if user != submit[0].user.nick:
		pageInfo = "the code is not yours!"
		title = '404 not found'
		return render_to_response('error.html', {'context':context, 'pageInfo':pageInfo, 'title':title})
	source = Source_code.objects.filter(solution_id=runid)
	return render_to_response('source.html', {'context':context, 'source':source[0], 'submit':submit[0]})

		
