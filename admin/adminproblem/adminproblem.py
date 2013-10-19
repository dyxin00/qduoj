#coding=utf-8

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from string import join,split
from django.core.paginator import Paginator
import os, os.path
from oj.models import *
from admin.is_login.is_login import *
from oj.qduoj_config.qduoj_config import *
from admin.uploadfile.uploadfile import *

def admin_problem_list_sc(req, page, context):
	is_ok = is_manager_login(req, context)
	if is_ok == 0:
		return HttpResponseRedirect('/admin/admin_login')
	list_info = {}
	page_num = []
	page = int(page) 
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
	if req.method == 'POST':
		form = adminsearch(req.POST)
		if form.is_valid():
			proid = form.cleaned_data['search_id']
			problem = Problem.objects.filter(problem_id=proid)
			return render_to_response('admin_problem_list.html', {'problems':problem})
	else:
		form = adminsearch()
	problemset = p.page(page).object_list
	return render_to_response('admin_problem_list.html', {"problems":problemset, "context":context, 'list_info':list_info, 'form':form})

#fetch data form form and save if to the database
def fetch_form_to_data(req, form, fun, proid=''):
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
		problem = Problem(
				title=title, 
				time_limit=time_limit, 
				memory_limit=memory_limit, 
				description=description, 
				input_data=input_data, 
				output_data=output_data, 
				sample_input=sample_input, 
				sameple_output=sample_output,
				source=source, 
				hint=hint,
				hard=hard
				)
		problem.save()
		return problem
	else:
		problem = Problem.objects.filter(problem_id=proid)
		problem.update(
				title=title, 
				time_limit=time_limit, 
				memory_limit=memory_limit, 
				description=description, 
				input_data=input_data, 
				output_data=output_data, 
				sample_input=sample_input, 
				sameple_output=sample_output, 
				source=source,
				hint=hint, 
				hard=hard
				)

def fetch_data_to_form(req, problem):
	problem_info = {}
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
	return problem_info

def admin_add_problem_sc(req, context):
	is_ok = is_manager_login(req, context)
	if is_ok == 0:
		return HttpResponseRedirect('/admin/admin_login')
	if req.method == 'POST':
		form = admin_problem(req.POST)
		if form.is_valid():
			problem = fetch_form_to_data(req, form, fun='submit')
			#return HttpResponseRedirect('/admin/problem_list')
			return HttpResponseRedirect('/admin/if_add_data/proid=%s'%problem.problem_id)
	else:
		form = admin_problem()
	return render_to_response('admin_add_problem.html', {'context':context, 'form':form})

def admin_edit_problem_sc(req, proid, context):
	is_ok = is_manager_login(req, context)
	if is_ok == 0:
		return HttpResponseRedirect('/admin/admin_login')
	problem_info = {}
	problem = Problem.objects.filter(problem_id=proid)
	if len(problem) == 0:
		pageInfo = "page not found!"
		return render_to_response('error.html', {"pageInfo": pageInfo, "context":context})
	if req.method == 'POST':
		form = admin_problem(req.POST)
		if form.is_valid():
			fun = 'edit'
			fetch_form_to_data(req, form, fun, proid)
			return HttpResponseRedirect('/admin/problem_list')
	else:
		problem_info = fetch_data_to_form(req, problem[0])
		form = admin_problem(problem_info)
	return render_to_response('admin_edit_problem.html', {'form':form, 'context':context})

def problem_shift_mode_sc(req, proid, page, fun, context):
	is_ok = is_manager_login(req, context)
	if is_ok == 0:
		return HttpResponseRedirect('/admin/admin_login')
	problem = Problem.objects.filter(problem_id=proid)
	if len(problem) == 0:
		pageInfo = "no this problem"
		return render_to_response('error.html', {'context':context, 'pageInfo':pageInfo})
		
	if fun == 'visible':
		if problem[0].visible == True:
			problem.update(visible=False)
		else:
			problem.update(visible=True)
	elif fun == 'oi_mode':
		if problem[0].oi_mode == True:
			problem.update(oi_mode=False)
		else:
			problem.update(oi_mode=True)
	if page == '0':
		problem = Problem.objects.filter(problem_id=proid)
		return render_to_response('admin_problem_list.html', {'problems':problem})
	else:
		return HttpResponseRedirect('/admin/problem_list/page=%s' % page)

def if_add_data_sc(req, proid, context):
	is_ok = is_manager_login(req, context)
	if is_ok == 0:
		return HttpResponseRedirect('/admin/admin_login')
	targetDir = os.path.join(TEST_DATA_PATH, proid)
	if not os.path.exists(targetDir):
		os.makedirs(targetDir)
	problem = Problem.objects.filter(problem_id = proid)
	return render_to_response('admin_if_add_data.html', {'problem':problem[0]})


def problem_testdata_sc(req, proid, context):
	is_ok = is_manager_login(req, context)
	if is_ok == 0:
		return HttpResponseRedirect('/admin/admin_login')
	targetDir = os.path.join(TEST_DATA_PATH, proid)
	try:
		files = os.listdir(targetDir)
	except IOError:
		pageInfo = 'the problem %s not exist' % proid
		return render_to_response('admin_error.html', {'pageInfo':pageInfo})
	if req.method == 'POST':
		form = Admin_UploadFiles(req.POST, req.FILES)
		if form.is_valid():
			files = req.FILES['files']
			if files.size <= MAX_UPLOAD_FILE_SIZE * 1000000:
				print files.size
				handle_load_files(proid, req.FILES['files']) #error
				files = os.listdir(targetDir)
				return render_to_response('problem_filelist.html', {'files':files, 'proid':proid, 'form':form})	
			else:
				pageInfo = 'the file size exceed the max size 5M'	
				return render_to_response('admin_error.html', {'pageInfo':pageInfo})
	else:
		form = Admin_UploadFiles()
	return render_to_response('problem_filelist.html', {'files':files, 'proid':proid, 'form':form})

def delete_testdata_sc(req, proid, filename, context):
	(targetFile, is_file) = is_file_exists(req, proid, filename)
	if is_file == 0:
		pageInfo = 'the file %s not exist' % filename
		return render_to_response('admin_error.html', {'pageInfo':pageInfo})
	elif is_file == 1: #if 1, it is a file folder
		remove_file_folder(req, targetFile)
	else:
		os.remove(targetFile)
	return HttpResponseRedirect('/admin/problem_testdata/proid=%s'%proid)

def download_testfile_sc(req, proid, filename, context):
	(targetFile, is_file) = is_file_exists(req, proid, filename)
	if is_file == 0:
		pageInfo = 'the file %s not exist'%filename
		return render_to_response('admin_error.html', {'pageInfo':pageInfo})
	return downfile_via_url(req, targetFile, filename)
	
