#coding=utf-8
# function: rank, usr_info

from django.shortcuts import render_to_response
from oj.models import *
from oj.forms import *
from oj.qduoj_config.qduoj_config import *
from oj.util.util import *


def rank_sc(req, page, context):

    try:
        page = int(page)
    except ValueError:
        pageInfo = "page not found"
        title = '404 not found'
        return render_to_response('error.html',
                                  {'context':context,
                                   'pageInfo':pageInfo,
                                   'title':title})

    (users, list_info) = paging(User.objects.order_by('-ac', 'submit'),
                                                    PAGE_RANK_NUM,page)

    if users == None:
        pageInfo = 'page not found maybe you are far behind!'
        title = '404 not found'
        return render_to_response('error.html',
                                  {'pageInfo':pageInfo,
                                   'title':title, 'context':context})    

    k = 1
    for user in users:
        User.objects.filter(nick=user.nick).update(
            rank=(page - 1)*PAGE_RANK_NUM + k)
        k = k + 1
    return render_to_response('user_rank.html',
                              {'users':users,
                               'context':context,
                               'list_info':list_info})


def user_info_sc(req, nick, context):

    user = User.objects.filter(nick=nick)
    if len(user) == 0:
        pageInfo = "there is no this user!"
        title = '404 not found!'
        return render_to_response('error.html',
                                  {'pageInfo':pageInfo,
                                   'title':title,
                                   'context':context})

    submitions = Solution.objects.filter(user=user[0])

    submitAc_list = submitions.filter(result=4).values_list(
                        'problem_id', flat=True).distinct()
    submitnotac_list = submitions.exclude(result=4).values_list(
                        'problem_id', flat=True).distinct()
    not_solved = [val for val in submitnotac_list if val not in submitAc_list]

    return render_to_response('user_info.html', {'user':user[0],
                                                 'context':context,
                                                 'submitAc_list' :submitAc_list,
                                                 'not_solved':not_solved,
                                                })


def source_code_sc(req, runid, context):
    submit = Solution.objects.filter(solution_id=runid)
    if not 'ojlogin' in context or len(submit) == 0:
        pageInfo = "user not login or cant found the submit"
        title = "404 not found"
        return render_to_response('error.html',
                                  {'context':context,
                                   'pageInfo':pageInfo,
                                   'title':title})
    user = context['ojlogin'].nick
    if user != submit[0].user.nick:
        pageInfo = "the code is not yours!"
        title = '404 not found'
        return render_to_response('error.html',
                                  {'context':context,
                                   'pageInfo':pageInfo,
                                   'title':title})
    source = Source_code.objects.filter(solution_id=runid)
    return render_to_response('source.html',
                              {'context':context,
                               'source':source[0],
                               'submit':submit[0]})

        
