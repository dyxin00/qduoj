from django.http import HttpResponse
from django.shortcuts import render_to_response
import os, sys

from oj.models import *

path = os.path.abspath(os.path.dirname(sys.argv[0]))
path_config = path + '/oj/qduoj_config'

if not path_config in sys.path:
	sys.path.append(path_config)

from admin.main.main import *
from admin.news.news import *
from admin.is_login.is_login import *
from qduoj_config import *
from admin.adminproblem.adminproblem import *

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

def problem_list(req, page='1'):
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

def admin_edit_problem(req, proid):
	context = baseInfo(req)
	return admin_edit_problem_sc(req, proid, context)

def problem_visible(req, proid, page):
	context = baseInfo(req)
	fun = 'visible'
	return problem_shift_mode_sc(req, proid, page, fun, context)

def problem_oi_mode(req, proid, page):
	context = baseInfo(req)
	fun = 'oi_mode'
	return problem_shift_mode_sc(req, proid, page, fun, context)

def if_add_data(req, proid):
	context = baseInfo(req)
	return if_add_data_sc(req, proid, context)

def problem_testdata(req, proid):
	context = baseInfo(req)
	return problem_testdata_sc(req, proid, context)

def delete_testdata(req, proid, filename):
	context = baseInfo(req)
	return delete_testdata(req, proid, filename, context)
