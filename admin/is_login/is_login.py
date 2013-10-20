#coding=utf-8

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from admin.forms import *
from oj.models import *

def is_manager_login(req, context):
    if not 'ojlogin' in context:
        return 0
    if context['ojlogin'].isManager != 0:
        return 0
    return 1

def admin_login_sc(req, context):
    error = {}
    if req.method == 'POST':
        form = manager_login(req.POST)
        if form.is_valid():
            username = form.cleaned_data['name']
            password = form.cleaned_data['password']

            user = User.objects.filter(nick=username)
            if len(user) == 0 or user[0].isManager != 0:
                error_info = "此管理员不存在,请重新输入!"
                error['error'] = error_info
                return render_to_response('admin_login.html', {'form':form, 'error':error, 'context':context})
            
            user = user[0]
            if user.password != password:
                error_info ="管理员密码错误,请重新输入!"
                error['error'] =error_info
                return render_to_response('admin_login.html', {'form':form, 'error':error, 'context':context})
            u = {"username":username, "password":password, "ac":user.ac}
            logininfo = LoginLog(user=user, ip=req.META['REMOTE_ADDR'])
            logininfo.save()
            req.session['login'] = u
            return HttpResponseRedirect('/admin')
            #return render_to_response('welcome.html')
    else:
        form = manager_login()
    return render_to_response('admin_login.html', {'context':context, 'form':form, 'error':error})
    
