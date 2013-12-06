#!/usr/bin/env python
# coding=utf-8

from django.shortcuts import render_to_response
from oj.models import Contest, Solution,Problem,User, Contest_problem
from oj.util.util import paging, Result_dic, language_ab
from oj.qduoj_config.qduoj_config import PAGE_STATUS_NUM
from oj.tools import error


def status_sc(req, context, page, cid = -1):

    page = int(page)
    solution = Solution.objects.filter(
        contest_id=cid).order_by('-solution_id')
    (solution, list_info) = paging(solution, PAGE_STATUS_NUM, page)

    if solution == None:
        return error('404', 'page ', context, 'error.html')
    if cid == -1:
        return problem_status(req, context, solution, list_info)
    else:
        return contest_status_sc(req, context, solution, list_info, cid)

def search_handle(req,context, page, cid = -1):
    """return solution status"""
    page = int(page)

    if req.method == "GET":
        try:
            problem_id_s = req.GET['problem_id']
            if len(problem_id_s):
                problem_id = int(problem_id_s)
            else:
                problem_id = -1
            user = req.GET['user_id']
            language = int(req.GET['language'])
            jresult = int(req.GET['jresult'])

        except ValueError:
            return error('404', 'problem ', context, 'error.html')
    solution = Solution.objects.filter(contest_id=cid).order_by('-solution_id')

    try:
        if problem_id != -1:
            if cid != -1:
                #contest_id 特殊处理   
                problem_id = Contest_problem.objects.filter(
                    contest_id = cid).get(num=problem_id).problem_id
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
        return error('404', 'page ', context, 'error.html')
    if cid == -1:
        return problem_status(req, context, solution, list_info)
    else:
        return contest_status_sc(req, context, solution, list_info, cid)

def problem_status(req, context, solution, list_info):
    """return problem status"""
    return render_to_response('status.html',
                              {"context" : context,
                               'Result' : Result_dic,
                               'language_ab' : language_ab,
                               'solution' : solution,
                               'list_info':list_info,
                               'cid' :-1,
                               'get':req.GET
                              })

def contest_status_sc(req, context, solution, list_info, cid):
    """return contest status"""
    contest_problem = Contest_problem.objects.filter(contest_id = cid)
    try:
        contest = Contest.objects.get(contest_id = cid)
    except Contest.DoesNotExist:
        return error('contest','404',context, 'error.html')

    if not contest.open_rank and not ('ojlogin' in context and context['ojlogin'].isManager):
        return error('','contest status private',context, 'permissions_tips.html')

    for var in solution:
        try:
            contest_p = contest_problem.get(
                problem_id = var.problem.problem_id)
        except Contest_problem.DoesNotExist:
            return error('404','problem',context, 'error.html')

        var.problem.title = contest_p.num
    return render_to_response('contest_status.html',
                              {
                                  "context" : context,
                                  'Result' : Result_dic,
                                  'language_ab' : language_ab,
                                  'solution' : solution,
                                  'list_info':list_info,
                                  'contest':contest,
                                  'cid' : cid,
                                  'get' : req.GET
                              })

