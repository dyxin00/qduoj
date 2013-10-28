#coding=utf-8

from django.http import HttpResponse, HttpResponseRedirect
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
from oj.util.util import contest_end
from oj.status_problem.status_problem import status_sc, __search__

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
    return problemlist_sc(page, context)

def problem(req, num):
    context = base_info(req)
    return problem_sc(num, context)

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
    return problem_sc(pid, context)
#  修改
def problem_search(req):
    search = req.GET['search']
    context = base_info(req)
    problem_s = Problem.objects.filter(title = str(search))
    if len(problem_s):
        pid = problem_s[0].problem_id
        return problem_sc(pid, context)
    else:
        page_info = "problem not found!"
        title = "404 not found"
        return render_to_response('error.html', {"pageInfo":page_info,
                                           "title":title, "context":context})


#submit code
def submit_code(req, num='1'):
    context = base_info(req)
    return submit_code_sc(req, num, context)



def rank(req, page='1'):
    context = base_info(req)
    return rank_sc(req, page, context)

def user_info(req, nick):
    context = base_info(req)
    return user_info_sc(req, nick, context)

def status(req, page='1'):
    context = base_info(req)
    return status_sc(context, page, -1)

def status_search(req, page= '1'):
    context = base_info(req)
    if req.method == 'GET':
        return __search__(req,context, page, -1)

def source_code(req, runid):
    context = base_info(req)
    return source_code_sc(req, runid, context)

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
    return readmail_sc(req, fun, msgid, context)

def contest_list(req, page = '1'):

    context = base_info(req)
    return contest_list_sc(context, page)
def contest(req, cid):

    context = base_info(req)
    return contest_sc(context, cid)

def contest_problem(req, num, cid):
    context = base_info(req)
    return problem_sc(num, context, cid)

def contest_submit_code(req, num, cid):

    if not contest_end(cid):
        context = base_info(req)
        return submit_code_sc(req, num, context, cid)
    else:
        return render_to_response("error.html")

def contest_status(req, cid, page = '1'):
    context = base_info(req)
    return status_sc(context, page, cid)
def contest_rank(req, cid):
    context = base_info(req)
    return contest_rank_sc(context, cid)
def contest_status_search(req, cid, page = 1):
    context = base_info(req)
    return __search__(req, context, page, cid)

def compile_error(req, num):

    num = int(num)

    context = base_info(req)
    try:
        error = Compileinfo.objects.get(solution_id = num)
    except Compileinfo.DoesNotExist:

        page_info = ''
        title = '404 not found'
        return render_to_response('error.html',
                {'pageInfo':page_info, 'title':title, 'context':context})
    return render_to_response("compile_run_error.html",
                              {'context':context,"error":error})

def runtime_error(req, num):
    num = int(num)
    context = base_info(req)
    try:
        error = Runtimeinfo.objects.get(solution_id=num)
    except Runtimeinfo.DoesNotExist:
        page_info = ''
        title = '404 not found'
        return render_to_response('error.html',
                {'pageInfo':page_info, 'title':title, 'context':context})
    return render_to_response("compile_run_error.html",
                              {'context':context,'error':error})

