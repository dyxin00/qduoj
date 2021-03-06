# coding=utf-8

'''the superuser alter the user's priority of other usesr'''

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from oj.models import User, Perm
from admin.is_login.is_login import *
from oj.qduoj_config.qduoj_config import *
from admin.uploadfile.uploadfile import *
from admin.admin_backends import is_manager
from admin.forms import AdminSearch

@is_manager
def admin_list_sc(req, context):
    '''list all the admin'''
    if req.method == 'POST':
        form = AdminSearch(req.POST)
        if form.is_valid():
            nick = form.cleaned_data['nick']
            user = User.objects.filter(nick = nick)
            if len(user) == 0:
                pageInfo = 'the user %s not exists' % nick
                return render_to_response('admin_error.html', {
                    'pageInfo':pageInfo}
                    )
            return HttpResponseRedirect('/admin/set_priority/id=%s' % nick)
    else:
        form = AdminSearch()
    users = User.objects.exclude(perm=None)
    return render_to_response('admin_list.html', {
        'users':users,
        'form':form}
    )

def alter_priority(user, checklist):
    '''only the superuser can alter the admin's priority add or delete
       it is used in the function set_priority_sc
    '''
    permlist = user.get_all_permission
    for (k, v) in permlist.items():
        user.remove_perm(v)
    for permission in checklist:
        perm = Perm.objects.filter(name=permission)
        if len(perm) != 0:
            user.add_perm(perm[0])

@is_manager
def set_priority_sc(req, context, nick):
    user = User.objects.filter(nick = nick)
    if len(user) == 0:
        pageInfo = 'the user %s not exists' % nick
        return render_to_response('admin_error.html', {
            'pageInfo':pageInfo}
        )
    if req.method == 'POST':
        checklist = req.REQUEST.getlist('check_box')
        alter_priority(user[0], checklist)
        return HttpResponseRedirect('/admin/admin_list')
  
    else:
        perms = Perm.objects.all()
        permlist = user[0].get_all_permission 
        return render_to_response('admin_set_priority.html', {
            'permlist':permlist,
            'user':user[0],
            'perms':perms
        })
    
