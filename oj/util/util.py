#coding=utf-8
from django.http import HttpResponseRedirect
from datetime import datetime, timedelta
from functools import wraps
from oj.models import Contest, Problem
from django.core.paginator import Paginator
from oj.tools import error

Result_dic = {

        4 : 'Accpepted',
        5 : 'Presentation Error',
        6 : 'Wrong Answer',
        7 : 'Time Limit Exceeded',
        8 : 'Memory Limit Exceeded',
        9 : 'Output Limit Exceeded',
        10: 'Runtime Error',
        11: 'Compile Error',
        3 : 'RJ',
        2 : 'CI',
        1 : 'Pending'
        }
language_ab = {
        0: 'C',
        1: 'C++'
        }
#page_number 多少一页
#page 第几页
def paging(tuple_info, page_number, page):
    
    page_num = []
    list_info = {}
    p = Paginator(tuple_info, page_number);

    if p.num_pages < 10:
        start = 0
        end = p.num_pages
    elif page <= 5:
        start = 0
        end = 10
    elif page >= p.num_pages - 5:
        start = p.num_pages - 10
        end = p.num_pages
    else:
        start = page - 5
        end = page + 5
        

    for i in range(start, end):
        page_num.append(i + 1)
    list_info['len'] = page_num
    list_info['page'] = page

    if page <= 0 or page > p.num_pages:
        return (None,None)
    else:
        info = p.page(page).object_list
        return (info,list_info)

def if_contest_end(function):
    @wraps(function)
    def wrapper(req, context, cid, *args, **kwargs):
        if cid > 0:
            try:
                contest_end_time = Contest.objects.get(contest_id = cid).end__time
            except Contest.DoesNotExist:
                return error('404', 'contest', context, 'error.html')           
            server_time = datetime.now()
            contest_end_time = contest_end_time.replace(
                tzinfo=None) + timedelta(hours=8)
            if server_time < contest_end_time or(
                'ojlogin' in context and context['ojlogin'].isManager):
                return function(req, context, cid, *args, **kwargs)
            else:
                return error('404', 'contest', context, 'error.html')
        else:
                return function(req, context, cid, *args, **kwargs)
    return wrapper
def if_contest_start(function):
    @wraps(function)
    def wrapper(context, cid, *args, **kwargs):
        cid = int(cid)
        try:
            contest_start_time = Contest.objects.get(contest_id = cid).start_time
        except:
            return error('404', 'contest', context, 'error.html')           
        server_time = datetime.now()
        contest_start_time = contest_start_time.replace(
                tzinfo=None) + timedelta(hours=8)
        if server_time >= contest_start_time or (
            'ojlogin' in context and context['ojlogin'].isManager):
            return function(context, cid, *args, **kwargs)
        else:
            return error('404', 'contest', context, 'error.html')           
    return wrapper
'''
def problem_permission(function):
    @wraps(function)
    def wrapper(context, num, cid = -1):
        pid = int(num)
        problem = Problem.objects.get(problem_id=pid)
        
'''
'''               
def contest_end(cid):
    try:
        contest_end_time = Contest.objects.get(contest_id = cid).end__time
    except Contest.DoesNotExist:
        return True
    server_time = datetime.now()
    contest_end_time = contest_end_time.replace(
        tzinfo=None) + timedelta(hours=8,minutes=1)
    
    if server_time < contest_end_time:
        return False
    else:
        return True
'''

def login_asked(function):
    @wraps(function)
    def wrapper(req, context, *args, **kwargs):
        if not 'ojlogin' in context:
            return HttpResponseRedirect('/oj/userlogin')
        else:
            return function(req, context, *args, **kwargs)
    return wrapper
