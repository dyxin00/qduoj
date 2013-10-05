#coding=utf-8

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from oj.models import *
from oj.forms import *
from django.core import serializers
from string import join,split

def problem_sc(req, num, context):
	
	try:
		ID = int(num)
		problem = Problem.objects.get(problem_id = ID)

		if problem.visible == False:
			pageInfo ="problem not found!"
			title = "404 not found"
			return render_to_response('error.html', {"pageInfo":pageInfo, "title":title, "context":context})

		problem_ab = problem_Handle(problem)
		return render_to_response('problem.html', {"problem":problem, "context":context,"problem_ab" : problem_ab})

	except Problem.DoesNotExist:

		pageInfo ="problem not found!"
		title = "404 not found"
		return render_to_response('error.html', {"pageInfo":pageInfo, "title":title, "context":context})
	except ValueError: 
		pageInfo ="problem not found!"
		title = "404 not found"
		return render_to_response('error.html', {"pageInfo":pageInfo, "title":title, "context":context})


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

def submit_code_sc(req,num,context):

	if req.method == 'POST':
		form_code = Submit_code(req.POST)
		if form_code.is_valid():
			submit_code = form_code.cleaned_data['submit_code']
			language_code = form_code.cleaned_data['language']
		
			if 'login' in req.session:   # wei chu li yi chang 
				if len(submit_code):
					solution = Solution.objects.create(

							result = 1,
							problem=Problem.objects.get(problem_id=int(num)),
							user = User.objects.get(nick=req.session['login']['username']),
							code_length = len(submit_code),
							language = int(language_code)
							)
					solution.save()
					source = Source_code.objects.create(

							solution_id =  int(solution.solution_id),
							code = submit_code 
							)
					source.save()
				
					return problem_sc(req,int(language_code),context) # 提交成功跳转
			else:
				pass # 未登录跳转
		else:
			error = 'Code too short!'
			return render_to_response('submit_code.html',{"form_code":form_code,"context":context,"error":error,"num":num})#submit_code  未添加
			
	else:
		form_code = Submit_code()

	return render_to_response('submit_code.html',{"num" : num,"form_code":form_code,"context" : context})

def status_sc(req,context):
	if req.method == 'POST':
		problem_id = int(req.POST['problem_id'])
		language = int(req.POST['language'])
		user_id = req.POST['user_id']
		jresult = int(req.POST['jresult'])
	else:
		form_status = Status()

	return render_to_response('status.html',{"context" : context})

def problem_Handle(problem):
	ab = {}

	ab['description'] = '<br>'.join( problem.description.split('\r\n'))
	ab['input_data'] = '<br>'.join( problem.input_data.split('\r\n'))
	ab['output_data'] = '<br>'.join( problem.output_data.split('\r\n'))
	ab['sample_input'] = '<br>'.join( problem.sample_input.split('\r\n'))
	ab['sameple_output'] = '<br>'.join( problem.sameple_output.split('\r\n'))

	return ab
