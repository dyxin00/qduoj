from django.shortcuts import render_to_response
from admin.is_login.is_login import *
from admin.admin_backends import has_any_perm
    
@has_any_perm
def index_sc(req, context):
    return render_to_response('admin_index.html', {
        'context':context}
    )

@has_any_perm
def oj_sc(req, context):
    return HttpResponseRedirect('/')

@has_any_perm
def menu_sc(req, context):
    permlist = context['ojlogin'].get_all_permission
    return render_to_response('admin_menu.html', {
        'context':context,
        'permlist':permlist}
    )

@has_any_perm
def welcome_sc(req, context):
    return render_to_response('welcome.html', {
        'context':context}
    )
