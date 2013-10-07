#coding=utf-8

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from oj.models import *
from oj.forms import *
from django.core import serializers
import sys, os


def login_sc(req, context):
	error = {}
	if req.method == 'POST':
		form = Login(req.POST)
		if form.is_valid():
			username = form.cleaned_data['name']
			password = form.cleaned_data['password']

			user = User.objects.filter(nick=username)
			if len(user) == 0:
				error_info = "用户名错误,请重新输入!"
				error['error'] = error_info
				return render_to_response('login.html', {'form':form, 'error':error, 'context':context})
			
			user = user[0]
			if user.password != password:
				error_info ="密码错误,请重新输入!"
				error['error'] =error_info
				return render_to_response('login.html', {'form':form, 'error':error, 'context':context})
			u = {"username":username, "password":password, "ac":user.ac}
			logininfo = LoginLog(user=user, ip=req.META['REMOTE_ADDR'])
			logininfo.save()
			req.session['login'] = u
			return HttpResponseRedirect('/')
	else:
		form = Login()
	return render_to_response('login.html', {'form':form, 'error':error, 'context':context})

def register_sc(req, context):
	error={}
	if req.method == "POST":
		form = Register(req.POST)
		if form.is_valid():
			username = form.cleaned_data['name']
			user = User.objects.filter(nick=username)
			if len(user) != 0:
				error_info = "该用户已存在！"
				error['error'] = error_info
			else:
				password = form.cleaned_data['password']
				email = form.cleaned_data['email']
				web_site = form.cleaned_data['website']
				user_register = User.objects.create(nick=username, password=password, email=email,website=web_site)
				user_register.save()
				url = '/' 
				info = '注册成功,'
				return render_to_response('jump.html', {'url':url, 'info':info, 'context':context})
	else:
		form = Register()
	return render_to_response('register.html', {'form':form, 'error':error, 'context':context})

def logout_sc(req):
	del req.session['login']
	url = '/'
	info = "成功退出!"
	return render_to_response('jump.html', {'url':url, 'info':info})





