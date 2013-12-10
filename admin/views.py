from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from oj.models import User, Problem, Contest
from admin.main.main import *
from admin.news.news import *
from admin.is_login.is_login import *
from admin.adminproblem.adminproblem import *
from admin.administer.administer import *
from admin.contest.contest import *
from admin.admin_shift_mode import admin_shift_mode_sc

def base_info(req):
    '''save the base_info of the user'''
    context = {}
    if 'login' in req.session:
        nick = req.session['login']['username']
        context['ojlogin'] = User.objects.get(nick=nick)
        req.session.set_expiry(1200)
    return context

def index(req):
    '''the first requst when the admin login'''
   # name1 = 'minister'
   # describe1 = 'priority: have priority to edit the contest or the problem ...'
   # perm1 = Perm.objects.create(name = name1, describe = describe1)
   # perm1.save()
    context = base_info(req)
    print type(index_sc)
    return index_sc(req, context)

def menu(req):
    '''the shift button page of the admin'''
    context = base_info(req)
    return menu_sc(req, context)

def welcome(req):
    '''the welcome requst when admin login'''
    context = base_info(req)
    return welcome_sc(req, context)

def admin_login(req):
    '''if the admin not login, login first!'''
    context = base_info(req)
    return admin_login_sc(req, context)

def news(req):
    '''the news list of the database'''
    context = base_info(req)
    return news_sc(req, context)

def add_news(req):
    '''add the fresh news for the web'''
    context = base_info(req)
    return add_news_sc(req, context)

def edit_news(req, msgid):
    '''get the news id via it can edit the news admin want'''
    context = base_info(req)
    return edit_news_sc(req, context, msgid)

def news_visible(req, msgid):
    '''get the news id set the news's visiblity'''
    context = base_info(req)
    return news_visible_sc(req, context, msgid)

def problem_list(req, page='1'):
    '''
    show all the problem saved in the db,
    default page is 1
    '''
    context = base_info(req)
    return admin_problem_list_sc(req, context, page)

def add_problem(req):
    '''
    add the new problem
    '''
    context = base_info(req)
    return admin_add_problem_sc(req, context)

def admin_edit_problem(req, proid):
    '''get problem id and edit it'''
    context = base_info(req)
    return admin_edit_problem_sc(req, context, proid)

#------------------------Admin shift mode --------------------------
def after_shift_mode(page, proid):
    if page == '0':
        problem = Problem.objects.filter(problem_id=proid) 
        return render_to_response('admin_problem_list.html',{
            'problems':problem}
        )
    else:
        return HttpResponseRedirect(
            '/admin/problem_list/page=%s' % page
            )
    
def problem_shift_mode(req, proid, page, fun):
    '''
    get problem id, set it's mode it cotains
    the problem's visiblity and the os_mode
    '''
    problem = Problem.objects.filter(problem_id=proid)
    context = base_info(req)
    admin_shift_mode_sc(req, context, problem, fun)
    return after_shift_mode(page, proid)

def contest_shift_mode(req, conid, page, fun):
    '''
    get contest id, set  it's mode it contains
    the contest's visibility and the oi_mode private and open_rank
    '''
    contest = Contest.objects.filter(contest_id=conid)
    context = base_info(req)
    admin_shift_mode_sc(req, context, contest, fun)
    return HttpResponseRedirect(
        '/admin/contest_list/page=%s' % page
        )

#--------------------------------------------------------------------

def if_add_data(req, proid):
    '''
    after you add a problem, choose whether add testdata for
    it
    '''
    context = base_info(req)
    return if_add_data_sc(req, context, proid)

def problem_testdata(req, proid):
    '''
    get the problem id,
    show the list testdata of the problem
    '''
    context = base_info(req)
    return problem_testdata_sc(req, context, proid)

def delete_testdata(req, proid, filename):
    context = base_info(req)
    return delete_testdata_sc(req, context, proid, filename)

def download_testfile(req, proid, filename):
    '''
    via clicking the link on the page, download the testdata
    '''
    context = base_info(req)
    return download_testfile_sc(req, context, proid, filename)

def admin_list(req):
    context = base_info(req)
    return admin_list_sc(req, context)

def set_priority(req, nick):
    context = base_info(req)
    return set_priority_sc(req, context, nick)

def rejudge(req):
    context = base_info(req)
    return rejudge_sc(req, context)

def contest_list(req, page=1):
    context = base_info(req)
    return contest_list_sc(req, context, page)
