# coding=utf-8

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
    users = User.objects.all()
    return render_to_response('admin_list.html', {
        'users':users,
        'form':form}
    )

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
        print checklist
        return render_to_response('admin_error.html')
        
    else:
        perms = Perm.objects.all()
        permlist = user[0].get_all_permission 
        return render_to_response('admin_set_priority.html', {
            'permlist':permlist,
            'user':user[0],
            'perms':perms
        })
    
