#!/usr/bin/env python
# coding=utf-8

from django.shortcuts import render_to_response
from oj.models import Contest, Solution,Problem,User, Contest_problem
from oj.util.util import paging, Result_dic, language_ab
from oj.qduoj_config.qduoj_config import PAGE_STATUS_NUM


def status_sc(context, page, cid = -1):
    page = int(page)

    solution = Solution.objects.filter(
        contest_id=cid).order_by('-solution_id')
    (solution, list_info) = paging(solution, PAGE_STATUS_NUM, page)

    if solution == None:
        page_info = "page not found!!"
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

def __search__(req,context, page, cid = -1):
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
            page_info = "problem not found!"
            title = "404 not found"
            return render_to_response('error.html',
                                  {"pageInfo":page_info, "title":title, "context":context})

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
                               'list_info':list_info,
                               'cid' :-1
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
        except Contest_problem.DoesNotExist:
            pass
        var.problem.title = contest_p.title
    return render_to_response('contest_status.html',
                              {
                                  "context" : context,
                                  'Result' : Result_dic,
                                  'language_ab' : language_ab,
                                  'solution' : solution,
                                  'list_info':list_info,
                                  'contest':contest,
                                  'cid' : cid
                              })

