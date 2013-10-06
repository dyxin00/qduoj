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

if not path_pro in sys.path:
	sys.path.append(path_pro)
if not path_login in sys.path:
	sys.path.append(path_login)
if not path_status_rank in sys.path:
	sys.path.append(path_status_rank)

from problem import *
from login_register import *
from status_rank import *

def baseInfo(req):    #the news and the session!
	context = {}
	news = News.objects.order_by("-time");
	if len(news) > 3:
		news = news[0:3]
	print "1"
#	print req.session['ojlogin']
	context['news'] = news

	if 'login' in req.session:
		context['ojlogin'] = User.objects.get(nick=req.session['login']['username'])
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

def rank(req, page='1'):
	context = baseInfo(req)
	return rank_sc(req, page, context)
	
