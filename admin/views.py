from django.http import HttpResponse
from django.shortcuts import render_to_response
import os, sys
from oj.models import *

path = os.path.abspath(os.path.dirname(sys.argv[0]))
path_main = path + '/admin/main'
path_news = path + '/admin/news'
path_islogin = path + '/admin/is_login'
path_config = path + '/oj/qduoj_config'
path_problem = path + '/admin/adminproblem'

if not path_main in sys.path:
	sys.path.append(path_main)
if not path_news in sys.path:
	sys.path.append(path_news)
if not path_islogin in sys.path:
	sys.path.append(path_islogin)
if not path_config in sys.path:
	sys.path.append(path_config)
if not path_problem in sys.path:
	sys.path.append(path_problem)

from main import *
from news import *
from is_login import *
from qduoj_config import *
from adminproblem import *

def baseInfo(req):
	context = {}
	if 'login' in req.session:
		context['ojlogin'] = User.objects.get(nick=req.session['login']['username'])
		req.session.set_expiry(1200)
	return context

def index(req):
	context = baseInfo(req)
	return index_sc(req, context)

def oj(req):
	context = baseInfo(req)
	return oj_sc(req, context)

def menu(req):
	context = baseInfo(req)
	return menu_sc(req, context)

def welcome(req):
	context = baseInfo(req)
	return welcome_sc(req, context)

def admin_login(req):
	context = baseInfo(req)
	return admin_login_sc(req, context)

def news(req):
	context = baseInfo(req)
	return news_sc(req, context)

def add_news(req):
	context = baseInfo(req)
	return add_news_sc(req, context)

def edit_news(req, msgid):
	context = baseInfo(req)
	return edit_news_sc(req, msgid, context)

def news_visible(req, msgid):
	context = baseInfo(req)
	return news_visible_sc(req, msgid, context)

def problem_list(req, page = "1"):
	print page
	context = baseInfo(req)
	return admin_problem_list_sc(req, page, context)

def add_problem(req):
	context = baseInfo(req)
	return admin_add_problem_sc(req, context)

def admin_search(req):
	context = baseInfo(req)
	proid = req.GET['search_id']
	return admin_search_sc(req, proid, context)

def admin_edit_problem_sc(req, proid, context):
	context = baseInfo(req)
	return admin_edit_problem_sc(req, proid, context)

