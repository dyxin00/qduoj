from oj.models import *
from oj.qduoj_config.qduoj_config import *
from admin.main.main import *
from admin.news.news import *
from admin.is_login.is_login import *
from admin.adminproblem.adminproblem import *

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
    context = base_info(req)
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
    return edit_news_sc(req, msgid, context)

def news_visible(req, msgid):
    '''get the news id set the news's visiblity'''
    context = base_info(req)
    return news_visible_sc(req, msgid, context)

def problem_list(req, page='1'):
    '''
    show all the problem saved in the db,
    default page is 1
    '''
    context = base_info(req)
    return admin_problem_list_sc(req, page, context)

def add_problem(req):
    '''
    add the new problem
    '''
    context = base_info(req)
    return admin_add_problem_sc(req, context)

def admin_edit_problem(req, proid):
    '''get problem id and edit it'''
    context = base_info(req)
    return admin_edit_problem_sc(req, proid, context)

def problem_visible(req, proid, page):
    '''get problem id, set it's visibility'''
    context = base_info(req)
    fun = 'visible'
    return problem_shift_mode_sc(req, proid, page, fun, context)

def problem_oi_mode(req, proid, page):
    '''
    the qduoj has two mod when it runs, one is if one testdata is wrong,
    the result is wrong , the other is you can get scores from the right
    testdata
    '''
    context = base_info(req)
    fun = 'oi_mode'
    return problem_shift_mode_sc(req, proid, page, fun, context)

def if_add_data(req, proid):
    '''
    after you add a problem, choose whether add testdata for
    it
    '''
    context = base_info(req)
    return if_add_data_sc(req, proid, context)

def problem_testdata(req, proid):
    '''
    get the problem id,
    show the list testdata of the problem
    '''
    context = base_info(req)
    return problem_testdata_sc(req, proid, context)

def delete_testdata(req, proid, filename):
    context = base_info(req)
    return delete_testdata_sc(req, proid, filename, context)

def download_testfile(req, proid, filename):
    '''
    via clicking the link on the page, download the testdata
    '''
    context = base_info(req)
    return download_testfile_sc(req, proid, filename, context)
