#/usr/bin/env/python
#coding=utf-8

"""problem"""
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from oj.models import Problem, User, Solution, Source_code
from oj.forms import Submit_code
from oj.qduoj_config.qduoj_config import PAGE_PROBLEM_NUM
from oj.util.util import paging, contest_end

def problem_sc(num, context, cid = -1):
    """return  problem response"""
    try:
        pid = int(num)
        problem = Problem.objects.get(problem_id = pid)

        if problem.visible == False and cid == -1:
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

    page = int(page)
    ac_list = []
    (problemset, list_info) = paging(Problem.objects.order_by('problem_id'),
                                    PAGE_PROBLEM_NUM,page)
    if 'ojlogin' in context:
        user = context['ojlogin'].nick
        solution_ac = Solution.objects.filter(result=4)

        solution_ac = solution_ac.filter(user_id = User.objects.get(nick = user))
        ac_list = solution_ac.values_list('problem_id', flat=True).distinct()

    if problemset == None:
        page_info = "page not found!"
        title = "404 not found"
        return render_to_response('error.html', {"pageInfo": page_info,
                                    "title":title, "context":context})

    return render_to_response('problemlist.html',
                              {"problemset":problemset,
                               "context":context,
                               "ac_list" : ac_list,
                               'list_info':list_info})

def submit_code_sc(req, num, context, cid = -1):
    """sava code from database"""

    if cid > 0 and contest_end(cid):
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


def problem_handle(problem):
    """Handle problem"""
    pab = {}
    pab['description'] = '<br>'.join( problem.description.split('\r\n'))
    pab['input_data'] = '<br>'.join( problem.input_data.split('\r\n'))
    pab['output_data'] = '<br>'.join( problem.output_data.split('\r\n'))
    pab['sample_input'] = '<br>'.join( problem.sample_input.split('\r\n'))
    pab['sameple_output'] = '<br>'.join( problem.sample_output.split('\r\n'))
    return pab
