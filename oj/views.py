#coding=utf-8

from django.shortcuts import render_to_response
from oj.models import *
from oj.forms import *

from oj.problem.problem import *
from oj.login_register.login_register import *
from oj.status_rank.status_rank import *
from oj.change_info.change_info import *
from oj.usermail.usermail import *
from oj.qduoj_config.qduoj_config import *
from oj.contest.contest import *
from oj.status_problem.status_problem import status_sc, search_handle
from oj.tools import error

def base_info(req):    #the news and the session!
    context = {}
    news = News.objects.order_by("-time")
    if len(news) > 3:
        news = news[0:3]
#   print req.session['ojlogin']
    context['news'] = news

    if 'login' in req.session:
        mail_count = Mail.objects.filter(mail_to=req.
                    session['login']['username']).filter(is_new=True).count()
        context['mail_count'] = mail_count
        context['ojlogin'] = User.objects.get(
            nick=req.session['login']['username'])
        req.session.set_expiry(1200)
    return context

def problemlist(req, page = "1"):
    context = base_info(req)
    return problemlist_sc(req, page, context)

def problem(req, num):
    context = base_info(req)
    return problem_sc(context=context, num=num, cid=-1)

def login(req):
    context = base_info(req)
    return login_sc(req, context)

def register(req):
    context = base_info(req)
    return register_sc(req, context)

def logout(req):
    return logout_sc(req)

# search
def problemid(req):
    pid = req.GET['id']
    context = base_info(req)
    return problem_sc(context=context, num=pid, cid=-1)
#  修改
def problem_search(req):
    search = req.GET['search']
    context = base_info(req)
    problem_s = Problem.objects.filter(title = str(search))
    if len(problem_s):
        pid = problem_s[0].problem_id
        return problem_sc(context=context, num=pid, cid=-1)
    else:
        return error('search', 'problem', context, 'error.html')


#submit code
def submit_code(req, num='1'):
    context = base_info(req)
    return submit_code_sc(req, context, -1, num)

def rank(req, page='1'):
    context = base_info(req)
    return rank_sc(req, page, context)

def user_info(req, nick):
    context = base_info(req)
    return user_info_sc(req, nick, context)

def status(req, page='1'):
    context = base_info(req)
    return status_sc(req, context, page, -1)

def status_search(req, page= '1'):
    context = base_info(req)
    if req.method == 'GET':
        return search_handle(req,context, page, -1)

def source_code(req, runid):
    context = base_info(req)
    return source_code_sc(req, context, runid)

def changepw(req):
    context = base_info(req)
    return changepw_sc(req, context)

def changeinfo(req):
    context = base_info(req)
    return changeinfo_sc(req, context)

def mail(req, fun='1'):   #fun=1 all the mail  2 the new mail 3 sent mail
    context = base_info(req)
    if not 'ojlogin' in context:
        page_info = 'you must login first!'
        title = '404 not found'
        return render_to_response('error.html',
                    {'pageInfo':page_info, 'title':title, 'context':context})
    if fun == '4':
        return sendmail_sc(req, fun, context)
    return mail_sc(req, fun, context)

def readmail(req, fun, msgid):
    context = base_info(req)
    return readmail_sc(req, context, fun, msgid)

def contest_list(req, page = '1'):

    context = base_info(req)
    return contest_list_sc(context, page)
def contest(req, cid):

    context = base_info(req)
    return contest_sc(context=context, cid=cid)

def contest_problem(req, num, cid):
    context = base_info(req)
    return problem_sc(context=context, num=num, cid=cid)

def contest_submit_code(req, num, cid):
    context = base_info(req)
    return submit_code_sc(req, context, cid, num)

def contest_status(req, cid, page = '1'):
    context = base_info(req)
    return status_sc(req, context, page, cid)

def contest_rank(req, cid):
    context = base_info(req)
    return contest_rank_sc(context, cid)
def contest_status_search(req, cid, page = 1):
    context = base_info(req)
    return search_handle(req, context, page, cid)

def contest_rank_xls(req,cid):
    context = base_info(req)
    return contest_rank_xls_sc(context,cid)

def compile_error(req, num):
    num = int(num)
    context = base_info(req)
    try:
        c_error = Compileinfo.objects.get(solution_id = num)
    except Compileinfo.DoesNotExist:
        return error('Compile','Compile Error',context)
    
    return render_to_response("compile_run_error.html",
                              {'context':context,"error":c_error})

def runtime_error(req, num):
    num = int(num)
    context = base_info(req)
    try:
        r_error = Runtimeinfo.objects.get(solution_id=num)
    except Runtimeinfo.DoesNotExist:
        return error('Runtimeinfo','Runtimeinfo',context)
    return render_to_response("compile_run_error.html",
                              {'context':context,'error':r_error})

