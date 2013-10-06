#coding=utf-8

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from oj.models import *
from oj.forms import *
from django.core import serializers
import sys, os

def changepw_sc(req, context):
	error = {}
	if not 'ojlogin' in context:
		pageInfo = 'you must login first!'
		title = '404 not found'
		return render_to_response('error.html', {'pageInfo':pageInfo, 'title':title, 'context':context})
	if req.method == 'POST':
		form = ChangePw(req.POST)
		if form.is_valid():
			pw_current = form.cleaned_data['pw_current']
			user = User.objects.filter(nick=context['ojlogin'].nick)
			if user[0].password == pw_current:
				pw_now = form.cleaned_data['pw_now']
				user.update(password=pw_now)
				url = '/user_info/name='+user[0].nick
				info = 'change success!'
				return render_to_response('jump.html', {'url':url, 'info':info, 'context':context})
			else:
				error_info = "you enter the wrong password!"
				error['error'] = error_info
	else:
		form = ChangePw()
	return render_to_response('changepw.html', {'context':context, 'form':form, 'error':error})

def changeinfo_sc(req, context):
	if not 'ojlogin' in context:
		pageInfo = 'you must login first!'
		title = '404 not found'
		return render_to_response('error.html', {'pageInfo':pageInfo, 'title':title, 'context':context})

	user = User.objects.filter(nick=context['ojlogin'].nick)
	if req.method == 'POST':
		Email = req.POST['email']
		Website = req.POST['website']
		user.update(email=Email)
		user.update(website=Website)
		url = '/user_info/name='+user[0].nick
		info = 'change success!'
		return render_to_response('jump.html', {'url':url, 'info':info, 'context':context})
	return render_to_response('changeinfo.html', {'user':user[0], 'context':context})
