#coding=utf-8

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from oj.models import *
from oj.forms import *
from django.core import serializers
import sys, os


def mail_sc(req, fun, context):
'''	
	if not 'ojlogin' in context:
		pageInfo = 'you must login first!'
		title = '404 not found'
		return render_to_response('error.html', {'pageInfo':pageInfo, 'title':title, 'context':context})
'''	
	if fun <= 0 or fun > 3:
		pageInfo = 'the page not found!'
		title = '404 not found!'
		return render_to_response('error.html', {'pageInfo':pgeInfo, 'title':title, 'context':context})
	username = context['ojlogin'].nick
	if fun == 1:

#	mails = Mail.objects.extra(where=["mail_to=usrname", "is_new=False"])
	mails = Mail.objects.filter(mail_to=username)
	if len(mails) > 50:
		mails = mails[0:50]
	return render_to_response('mail.html', {'mails':mails, 'context':context})

