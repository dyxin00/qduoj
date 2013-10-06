#coding=utf-8

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from oj.models import *
from oj.forms import *
from django.core import serializers

def problem_sc(req, num, context):
	
	problem= Problem.objects.filter(problem_id=int(num))
	
	if problem[0] == None or problem[0].visible == False:
		pageInfo ="problem not found!"
		title = "404 not found"
		return render_to_response('error.html', {"pageInfo":pageInfo, "title":title, "context":context})
	
	return render_to_response('problem.html', {"problem":problem[0], "context":context})


def problemlist_sc(req, page, context):
	list_info = {}
	page_num = []
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
