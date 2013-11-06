#coding=utf-8
# function: rank, usr_info

from django.shortcuts import render_to_response
from oj.models import User, Solution, Source_code
from oj.qduoj_config.qduoj_config import PAGE_RANK_NUM
from oj.util.util import paging, login_asked
from oj.tools import error

def rank_sc(req, page, context):
    '''the rank of the user'''
    page = int(page)
    (users, list_info) = paging(User.objects.order_by('-ac', 'submit'),
                                PAGE_RANK_NUM, page)
    if users == None:
        return error('4o4', 'far behind, you ', context)

    k = 1
    for user in users:
        User.objects.filter(nick=user.nick).update(
            rank=(page - 1)*PAGE_RANK_NUM + k
            )
        k = k + 1
    return render_to_response('user_rank.html',
                              {'users':users,
                               'context':context,
                               'list_info':list_info})


def user_info_sc(req, nick, context):
    '''the base info of the user'''
    user = User.objects.filter(nick=nick)
    if len(user) == 0:
        return error('4o4', 'user ', context)
    submitions = Solution.objects.filter(user=user[0]).order_by('problem')

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


@login_asked
def source_code_sc(req, context, runid):
    '''fetch the source code '''
    submit = Solution.objects.filter(solution_id=runid)
    if len(submit) == 0:
        return error('4o4', 'code  ', context)
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

