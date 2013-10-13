#coding=utf-8

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from oj.models import *
from oj.forms import *
from django.core import serializers
import sys, os


def mail_sc(req, fun, context):
	username = context['ojlogin'].nick

	if fun == '1':
		mails = Mail.objects.filter(mail_to=username)
	elif fun == '2':
		mails = Mail.objects.extra(where=["mail_to=username", "is_new=True"])
	elif fun == '3':
		mails = Mail.objects.filter(mail_from=username)
	else:
		pageInfo = 'the page not found!'
		title = '404 not found!'
		return render_to_response('error.html', {'pageInfo':pageInfo, 'title':title, 'context':context})
	if len(mails) > 50:
		mails = mails[0:50]
	return render_to_response('mail.html', {'mails':mails, 'context':context, 'fun':fun})

def sendmail_sc(req, fun, context):
	error = {}
	if req.method == 'POST':
		form = Send_mail(req.POST)
		if form.is_valid():
			sentfrom = context['ojlogin'].nick
			sendto = form.cleaded_data['send_to']
			user = User.objects.filter(nick=sendto)
			if len(user) == 0:
				pageInfo = 'the user does not exits!'
				error['error'] = pageInfo
			title = form.cleaded_data['title']
			content = form.cleaned_data['content']
			mail = Mail.create(mail_from=sentfrom, mail_to=sendto, title=title, content=content, is_new=True)
			mail.save()
			url = "/mail"
			info = "send success!"
			return render_to_response('jump.html', {'context':context, 'url':url, 'info':info})
	else:
		form = Send_mail()
	return render_to_response('sendmail.html', {'context':context, 'form':form})
