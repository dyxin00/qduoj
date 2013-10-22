from django.http import HttpResponse, HttpResponseRedirect 
from django.shortcuts import render_to_response 
from oj.models import * 
from oj.forms import * 
from django.core import serializers 
from string import join,split 
from oj.qduoj_config.qduoj_config import *
from django.core.paginator import Paginator 
from oj.util.util import *

def contest_list_sc(req,context,page):

	list_info = {}
	page_num = []
	try:
		page = int(page)
	except ValueError:
		return render_to_response("error.html",{'pageinfo':'page not found!','title':'404 not found!'})

	(contest,list_info) = paging(Contest.objects.order_by("-contest_id"),PAGE_CONTEST_NUM,page)
	if contest == None:
		return render_to_response("error.html",{'pageinfo':'page not found!','title':'404 not found!'})


	return render_to_response("contest_list.html",{ "context" : context,"contest":contest,"list_info": list_info })

def contest_sc(req,context,cid):
	problem_list = [];

	try:
		cid = int(cid)
	except ValueError:
		return render_to_response("error.html",{'pageinfo':'page not found!','title':'404 not found!'})

	contest = Contest.objects.filter(contest_id = cid)
	problem = Contest_problem.objects.filter(contest_id = cid)
	
	contest_solution = Solution.objects.filter(contest_id = cid)
	for p in problem:
		p_contest_solution = contest_solution.filter(problem_id = p.problem_id)
		problem_list.append(
				{
					"problem_id" : p.problem_id,
					"num":p.num,
					"title" : p.title,
					"submit" : p_contest_solution.count(),
					"Ac" : p_contest_solution.filter(result = 4).count()
					}
				)

	return render_to_response("contest.html",{"context":context,"contest":contest[0],"problem_list" : problem_list})







