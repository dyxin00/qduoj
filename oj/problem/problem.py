#/usr/bin/env/python
#coding=utf-8

"""problem"""
#from django.http import HttpResponse, HttpResponseRedirect
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from oj.models import User, Problem, Solution, Source_code, Contest, Contest_problem
from oj.forms import Submit_code
#from django.core import serializers
#from string import join, split
from oj.qduoj_config.qduoj_config import PAGE_PROBLEM_NUM, PAGE_STATUS_NUM
from oj.util.util import paging, Result_dic, language_ab, contest_end

def problem_sc(num, context, cid = -1):
    """return  problem response"""
    try:
        pid = int(num)
        problem = Problem.objects.get(problem_id = pid)

        if problem.visible == False:
            page_info = "problem not found!"
            title = "404 not found"
            return render_to_response('error.html',
                    {"pageInfo":page_info, "title":title, "context":context})

        problem_ab = problem_handle(problem)
        return render_to_response('problem.html', {"problem":problem,
                        "context":context,"problem_ab" : problem_ab,"cid":cid})

    except Problem.DoesNotExist:

        page_info = "problem not found!"
        title = "404 not found"
        return render_to_response('error.html', {"pageInfo":page_info,
                                "title":title, "context":context})
    except ValueError:
        page_info = "page not found!"
        title = "404 not found"
        return render_to_response('error.html', {"pageInfo":page_info,
                                        "title":title, "context":context})


def problemlist_sc(page, context):
    """return problem_list response"""
    try:
        page = int(page) #抛异常
    except ValueError:
        page_info = "page not found!"
        title = "404 not found!"
        return render_to_response('error.html', {'pageInfo':page_info,
                                    'title':title, 'context':context})

    (problemset, list_info) = paging(Problem.objects.order_by('problem_id'),
                                    PAGE_PROBLEM_NUM,page)

    if problemset == None:
        page_info = "page not found!"
        title = "404 not found"
        return render_to_response('error.html', {"pageInfo": page_info,
                                    "title":title, "context":context})

    return render_to_response('problemlist.html', {"problemset":problemset,
                                 "context":context, 'list_info':list_info})

def submit_code_sc(req, num, context, cid = -1):
    """sava code from database"""

    if cid <= 0 or contest_end(cid):
        return render_to_response("error.html")
    if req.method == 'POST':
        form_code = Submit_code(req.POST)
        if form_code.is_valid():
            submit_code = form_code.cleaned_data['submit_code']
            language_code = form_code.cleaned_data['language']
            if 'login' in req.session:
                if len(submit_code):
                    user = User.objects.get(
                        nick=req.session['login']['username'])
                    solution = Solution.objects.create(

                            contest_id = int(cid),
                            result = 1,
                            problem=Problem.objects.get(problem_id=int(num)),
                            user = user,
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
                        return HttpResponseRedirect(
                            '/contest_status/cid=%s'%cid)
            else:
                error = 'Please login first!!'
                return render_to_response('submit_code.html',
                {"form_code":form_code,
                 "context":context,"error":error,"num":num})#未登录
        else:
            error = 'Code too short!'
            return render_to_response('submit_code.html',
                                      {"form_code":form_code,
                                       "context":context,
                                       "error":error,
                                        "num":num})#submit_code  未添加
    else:
        form_code = Submit_code()
    return render_to_response('submit_code.html',
                    {"num" : num,"form_code":form_code,"context" : context})

def status_sc(context, page, cid = -1, problem_id = -1,
              language = -1, user = '', jresult = -1):
    """return solution status"""
    try:
        page = int(page) #抛异常
    except ValueError:
        page_info = "page not found!"
        title = "404 not found!"
        return render_to_response('error.html',
                    {'pageInfo':page_info, 'title':title, 'context':context})

    solution = Solution.objects.filter(contest_id=cid).order_by('-solution_id')

    try:
        if problem_id != -1:
            solution = solution.filter(problem_id = Problem.objects.get(
                problem_id = problem_id))
        if len(user):
            User.objects.get(nick = user)
            solution = solution.filter(user = User.objects.get(nick = user))
        if language != -1:
            solution = solution.filter(language = language)
        if jresult != -1:
            solution = solution.filter(result = jresult)
    except User.DoesNotExist:
        return render_to_response('status.html', {"context" : context})

    (solution, list_info) = paging(solution, PAGE_STATUS_NUM, page)

    if solution == None:
        page_info = "page not found!"
        title = "404 not found"
        return render_to_response('error.html',
                        {"pageInfo": page_info,
                         "title":title,
                         "context":context
                        })


    if cid == -1:
        return problem_status(context, solution, list_info)
    else:
        return contest_status_sc(context, solution, list_info, cid)

def problem_status(context, solution, list_info):
    """return problem status"""
    return render_to_response('status.html',
                              {"context" : context,
                               'Result' : Result_dic,
                               'language_ab' : language_ab,
                               'solution' : solution,
                               'list_info':list_info
                              })

def contest_status_sc(context, solution, list_info, cid):
    """return contest status"""
    contest_problem = Contest_problem.objects.filter(contest_id = cid)
    try:
        contest = Contest.objects.get(contest_id = cid)
    except Contest.DoesNotExist:
        pass


    for var in solution:
        try:
            contest_p = contest_problem.get(
                problem_id = var.problem.problem_id)
        except contest_problem.DoesNotExits:
            pass
        var.problem.title = contest_p.title
    return render_to_response('contest_status.html',
                              {
                                  "context" : context,
                                  'Result' : Result_dic,
                                  'language_ab' : language_ab,
                                  'solution' : solution,
                                  'list_info':list_info,
                                  'contest':contest
                              })

def problem_handle(problem):
    """Handle problem"""
    pab = {}
    pab['description'] = '<br>'.join( problem.description.split('\r\n'))
    pab['input_data'] = '<br>'.join( problem.input_data.split('\r\n'))
    pab['output_data'] = '<br>'.join( problem.output_data.split('\r\n'))
    pab['sample_input'] = '<br>'.join( problem.sample_input.split('\r\n'))
    pab['sameple_output'] = '<br>'.join( problem.sameple_output.split('\r\n'))
    return pab
