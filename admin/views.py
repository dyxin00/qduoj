from django.http import HttpResponse
from django.shortcuts import render_to_response
import os, sys
from oj.models import *

path = os.path.abspath(os.path.dirname(sys.argv[0]))
path_main = path + '/admin/main'
path_news = path + '/admin/news'
path_islogin = path + '/admin/is_login'

if not path_main in sys.path:
	sys.path.append(path_main)
if not path_news in sys.path:
	sys.path.append(path_news)
if not path_islogin in sys.path:
	sys.path.append(path_islogin)

from main import *
from news import *
from is_login import *

def baseInfo(req):
	context = {}
	if 'login' in req.session:
		context['ojlogin'] = User.objects.get(nick=req.session['login']['username'])
		req.session.set_expiry(1200)
	return context

def index(req):
	context = baseInfo(req)
	return index_sc(req, context)

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

def edit_news(req):
	context = baseInfo(req)
