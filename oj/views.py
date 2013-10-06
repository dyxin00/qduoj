#coding=utf-8

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from oj.models import *
from oj.forms import *
from django.core import serializers

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

def index(req):
	hehe = "<a href = \"http://www.baidu.com\">nihao</a>"
	return render_to_response('problemlist.html', {"hehe":hehe})

def problemlist(req, page = "1"):
	list_info = {}
	page_num = []
	context = baseInfo(req)
	page = int(page)
	problem = Problem.objects.order_by('problem_id')
	pro_len = len(problem)
	for i in range(0, pro_len/100 + 1):
		page_num.append(i+1)
	list_info['len'] = page_num
	list_info['page'] = page
	#if the requst is out of bound, error!
	if page == 0 or (page - 1) * 100 > pro_len:
		pageInfo = "page not found!"
		title = "404 not found"
		return render_to_response('error.html', {"pageInfo": pageInfo, "title":title, "context":context})

	problemset  = problem[(page-1)*100:page*100-1]
	return render_to_response('problemlist.html', {"problemset":problemset, "context":context, 'list_info':list_info})

def problem(req, num):
	context = baseInfo(req)
	num = int(num)
	problem= Problem.objects.filter(problem_id=num)
	
	print problem
	if problem[0] == None or problem[0].visible == False:
		pageInfo ="problem not found!"
		title = "404 not found"
		return render_to_response('error.html', {"pageInfo":pageInfo, "title":title, "context":context})
	
	return render_to_response('problem.html', {"problem":problem[0], "context":context})

def login(req):
	error = {}
	context = baseInfo(req)
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

def register(req):
	error={}
	context = baseInfo(req)
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

def logout(req):
	del req.session['login']
	url = '/'
	info = "成功退出!"
	return render_to_response('jump.html', {'url':url, 'info':info})

