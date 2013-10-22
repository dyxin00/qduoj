#coding=utf-8

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from oj.models import *
from oj.forms import *
from django.core import serializers
from string import join,split
from oj.qduoj_config.qduoj_config import *
from django.core.paginator import Paginator
from oj.util.util import *

def problem_sc(req, num, context,cid = -1):
	
	try:
		ID = int(num)
		problem = Problem.objects.get(problem_id = ID)
	
		if problem.visible == False:
			pageInfo ="problem not found!"
			title = "404 not found"
			return render_to_response('error.html', {"pageInfo":pageInfo, "title":title, "context":context})

		problem_ab = problem_Handle(problem)
		return render_to_response('problem.html', {"problem":problem, "context":context,"problem_ab" : problem_ab,"cid":cid})

	except Problem.DoesNotExist:

		pageInfo ="problem not found!"
		title = "404 not found"
		return render_to_response('error.html', {"pageInfo":pageInfo, "title":title, "context":context})
	except ValueError: 
		pageInfo ="page not found!"
		title = "404 not found"
		return render_to_response('error.html', {"pageInfo":pageInfo, "title":title, "context":context})


def problemlist_sc(req, page, context):

	try:
		page = int(page) #抛异常
	except ValueError:
		pageInfo = "page not found!"
		title = "404 not found!"
		return render_to_response('error.html', {'pageInfo':pageInfo, 'title':title, 'context':context})

	(problemset,list_info) = paging(Problem.objects.order_by('problem_id'), PAGE_PROBLEM_NUM,page)

	if problemset == None:
		pageInfo = "page not found!"
		title = "404 not found"
		return render_to_response('error.html', {"pageInfo": pageInfo, "title":title, "context":context})

	return render_to_response('problemlist.html', {"problemset":problemset, "context":context, 'list_info':list_info})

def submit_code_sc(req,num,context,cid = -1):

	if req.method == 'POST':
		form_code = Submit_code(req.POST)
		if form_code.is_valid():
			submit_code = form_code.cleaned_data['submit_code']
			language_code = form_code.cleaned_data['language']
		
			if 'login' in req.session:   # wei chu li yi chang 
				if len(submit_code):
					solution = Solution.objects.create(

							contest_id = int(cid),
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
					if cid == -1:
						return HttpResponseRedirect('/status')
					else:
						return HttpResponseRedirect('/contest_status/cid=%s'%cid)
			else:
				error = 'Please login first!!'
				return render_to_response('submit_code.html',{"form_code":form_code,"context":context,"error":error,"num":num})#未登录
		else:
			error = 'Code too short!'
			return render_to_response('submit_code.html',{"form_code":form_code,"context":context,"error":error,"num":num})#submit_code  未添加
			
	else:
		form_code = Submit_code()
	return render_to_response('submit_code.html',{"num" : num,"form_code":form_code,"context" : context})


def status_sc(req,context, page,cid = -1,problem_id = -1,language = -1,user = '',jresult = -1):

	try:
		page = int(page) #抛异常
	except ValueError:
		pageInfo = "page not found!"
		title = "404 not found!"
		return render_to_response('error.html', {'pageInfo':pageInfo, 'title':title, 'context':context})

	solution = Solution.objects.filter(contest_id = cid).order_by('-solution_id')

	try:
		if problem_id != -1 :
			solution = solution.filter(problem_id = Problem.objects.get(problem_id = problem_id))
		if len(user):
			User.objects.get(nick = user)
			solution = solution.filter(user = User.objects.get(nick = user))
		if language != -1 :
			solution = solution.filter(language = language)
		if jresult != -1:
			solution = solution.filter(result = jresult)
	
	except User.DoesNotExist:
		return render_to_response('status.html',{"context" : context})

	(solution,list_info) = paging(solution,PAGE_STATUS_NUM,page)

	if solution == None:
		pageInfo = "page not found!"
		title = "404 not found"
		return render_to_response('error.html', {"pageInfo": pageInfo, "title":title, "context":context})


	if cid == -1:
		return problem_status(context,solution,list_info)
	else:
		return contest_status(context,solution,list_info,cid)

def problem_status(context,solution,list_info):

	return render_to_response('status.html',{"context" : context,'Result' : Result_dic,'language_ab' : language_ab, 'solution' : solution,'list_info':list_info})
	



def contest_status(context,solution,list_info,cid):

	contest_problem = Contest_problem.objects.filter(contest_id = cid)

	for V in solution:
		contest_p = contest_problem.get(problem_id = V.problem.problem_id)
		V.problem.title = contest_p.title 

	return render_to_response('contest_status.html',{"context" : context,'Result' : Result_dic,'language_ab' : language_ab, 'solution' : solution,'list_info':list_info,'cid':cid})
	
	



def problem_Handle(problem):
	ab = {}
	ab['description'] = '<br>'.join( problem.description.split('\r\n'))
	ab['input_data'] = '<br>'.join( problem.input_data.split('\r\n'))
	ab['output_data'] = '<br>'.join( problem.output_data.split('\r\n'))
	ab['sample_input'] = '<br>'.join( problem.sample_input.split('\r\n'))
	ab['sameple_output'] = '<br>'.join( problem.sameple_output.split('\r\n'))
	return ab
