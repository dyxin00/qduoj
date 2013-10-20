#coding=utf-8

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from string import join,split
from django.core.paginator import Paginator
from oj.models import *
from is_login import *
from qduoj_config import *

def admin_problem_list_sc(req, page, context):
	is_ok = is_manager_login(req, context)
	if is_ok == 0:
		return HttpResponseRedirect('/admin/admin_login')
	list_info = {}
	page_num = []
	try:
		page = int(page) #抛异常
	except ValueError:
		pageInfo = "page not found!"
		title = "404 not found!"
		return render_to_response('error.html', {'pageInfo':pageInfo, 'title':title, 'context':context})
	p = Paginator(Problem.objects.order_by('problem_id'), ADMIN_PAGE_PROBLEM_NUM)
	
	for i in range(0, p.num_pages):
		page_num.append(i+1)
	list_info['len'] = page_num
	list_info['page'] = page
	#if the requst is out of bound, error!
	if page == 0 or page > p.num_pages:
		pageInfo = "page not found!"
		title = "404 not found"
		return render_to_response('error.html', {"pageInfo": pageInfo, "title":title, "context":context})
		
	form = adminsearch()
	problemset = p.page(page).object_list
	return render_to_response('admin_problem_list.html', {"problems":problemset, "context":context, 'list_info':list_info, 'form':form})

def save_submit_problem(req, form, fun, proid=''):
	title = form.cleaned_data['title']
	time_limit = form.cleaned_data['time_limit']
	memory_limit = form.cleaned_data['memory_limit']
	hard = form.cleaned_data['hard']
	description = form.cleaned_data['description']
	input_data = form.cleaned_data['input_data']
	output_data = form.cleaned_data['output_data']
	sample_input = form.cleaned_data['sample_input']
	sample_output = form.cleaned_data['sample_output']
	source = form.cleaned_data['source']
	hint = form.cleaned_data['hint']
	if fun == 'submit':
		problem = Problem(title=title, time_limit=time_limit, memory_limit=memory_limit, description=description, input_data=input_data, output_data=output_data, sample_input=sample_input, sameple_output=sample_output, source=source, hint=hint, hard=hard)
		problem.save()
	else:
		problem = Problem.objects.filter(problem_id=proid)
		problem.update(title=title, time_limit=time_limit, memory_limit=memory_limit, description=description, input_data=input_data, output_data=output_data, sample_input=sample_input, sameple_output=sample_output, source=source, hint=hint, hard=hard)
	

def admin_add_problem_sc(req, context):
	is_ok = is_manager_login(req, context)
	if is_ok == 0:
		return HttpResponseRedirect('/admin/admin_login')
	if req.method == 'POST':
		form = admin_problem(req.POST)
		if form.is_valid():
			save_submit_problem(req, form, fun='submit')
			return HttpResponseRedirect('/admin/problem_list')
	else:
		form = admin_problem()
	return render_to_response('admin_add_problem.html', {'context':context, 'form':form})

def admin_search_sc(req, proid, context):
	problem = Problem.objects.filter(problem_id=proid)
	if len(problem) == 0:
		pageInfo = "page not found!"
		return render_to_response('error.html', {"pageInfo": pageInfo, "title":title, "context":context})
	return render_to_response('admin_problem_list.html', {'problems':problem})

def admin_edit_problem_sc(req, proid, context):
	problem_info = {}
	problem = Problem.objects.filter(problem_id=proid)
	if len(problem) == 0:
		pageInfo = "page not found!"
		return render_to_response('error.html', {"pageInfo": pageInfo, "title":title, "context":context})
	if req.method == 'POST':
		form = adminsearch(req.POST)
		if form.is_valid():
			save_submit_problem(req, form, proid, fun='edit')
			return HttpResponseRedirect('/admin/problem_list')
	else:
		problem = problem[0]
		problem_info['title'] = problem.title
		problem_info['time_limit'] = problem.time_limit
		problem_info['memory_limit'] = problem.memory_limit
		problem_info['description'] = problem.description
		problem_info['input_data'] = problem.input_data
		problem_info['output_data'] = problem.output_data
		problem_info['sample_input'] = problem.sample_input
		problem_info['sample_output'] = problem.sameple_output
		problem_info['source'] = problem.source
		problem_info['hint'] = problem.hint
		problem_info['hard'] = problem.hard
	
		form = adminsearch(problem_info)
	return render_to_response('')
