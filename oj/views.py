#coding=utf-8

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from oj.models import *
from oj.forms import *
from django.core import serializers
import sys, os

#append the path of the function
path = os.path.abspath(os.path.dirname(sys.argv[0]))
path_pro = path + '/oj/problem' 
path_login = path + '/oj/login_register'
path_status_rank = path + '/oj/status_rank'
path_change_info = path + '/oj/change_info'
path_mail = path + '/oj/usermail'

if not path_pro in sys.path:
	sys.path.append(path_pro)
if not path_login in sys.path:
	sys.path.append(path_login)
if not path_status_rank in sys.path:
	sys.path.append(path_status_rank)
if not path_change_info in sys.path:
	sys.path.append(path_change_info)
if not path_mail in sys.path:
	sys.path.append(path_mail)

from problem import *
from login_register import *
from status_rank import *
from change_info import *
from usermail import *

def baseInfo(req):    #the news and the session!
	context = {}
	news = News.objects.order_by("-time");
	if len(news) > 3:
		news = news[0:3]
#	print req.session['ojlogin']
	context['news'] = news

	if 'login' in req.session:
		context['ojlogin'] = User.objects.get(nick=req.session['login']['username'])
		req.session.set_expiry(1200)
	return context

def problemlist(req, page = "1"):
	context = baseInfo(req)
	return problemlist_sc(req, page, context)

def problem(req, num):
	context = baseInfo(req)
	return problem_sc(req, num, context)

def login(req):
	context = baseInfo(req)
	return login_sc(req, context)

def register(req):
	context = baseInfo(req)
	return register_sc(req, context)

def logout(req):
	return logout_sc(req)

def problemId(req):
	ID = req.GET['id']
	context = baseInfo(req)
	return problem_sc(req,ID,context)

def problem_search(req):
	search = req.GET['search']
	context = baseInfo(req)
	problem = Problem.objects.filter(title = str(search))

	if len(problem):
		ID = problem[0].problem_id
		return problem_sc(req,ID,context)
	else:
		pageInfo ="problem not found!"
		title = "404 not found"
		return render_to_response('error.html', {"pageInfo":pageInfo, "title":title, "context":context})


def submit_code(req,num='1'):
	context = baseInfo(req)
	return submit_code_sc(req,num,context)



def rank(req, page='1'):
	context = baseInfo(req)
	return rank_sc(req, page, context)

def user_info(req, nick):
	context = baseInfo(req)
	return user_info_sc(req, nick, context)
	
def status(req, page='1'):
	context = baseInfo(req)
	return status_sc(req, context, page)

def status_Search(req, page='1'):
	context = baseInfo(req)
	if req.method == 'GET':
		problem_id = -1
		try:
			problem_id_s = req.GET['problem_id']
			if len(problem_id_s):
				problem_id = int(problem_id_s)
			else:
				problem_id = -1
			user_id = req.GET['user_id']

			language = int(req.GET['language'])
			jresult = int(req.GET['jresult'])

		except ValueError:
			pageInfo ="problem not found!"
			title = "404 not found"
			return render_to_response('error.html', {"pageInfo":pageInfo, "title":title, "context":context})

		return status_sc(req, context, page, problem_id, language, user_id, jresult)

def source_code(req, runid):
	context = baseInfo(req)
	return source_code_sc(req, runid, context)

def changepw(req):
	context = baseInfo(req)
	return changepw_sc(req, context)

def changeinfo(req):
	context = baseInfo(req)
	return changeinfo_sc(req, context)

def mail(req, fun='1'):   #fun=1 all the mail  2 the new mail 3 sent mail
	context = baseInfo(req)
	if not 'ojlogin' in context:
		pageInfo = 'you must login first!'
		title = '404 not found'
		return render_to_response('error.html', {'pageInfo':pageInfo, 'title':title, 'context':context})
	if fun == '4':
		return sendmail_sc(req, fun, context)
	return mail_sc(req, fun, context)
