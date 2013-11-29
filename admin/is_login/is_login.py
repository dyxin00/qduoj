#coding=utf-8

from django.http import  HttpResponseRedirect
from django.shortcuts import render_to_response
from admin.forms import manager_login 
from oj.tools import verify_user


def admin_login_sc(req, context):
    error = {}
    if req.method == 'POST':
        form = manager_login(req.POST)
        if form.is_valid():
            username = form.cleaned_data['name']
            password = form.cleaned_data['password']
            (status, run_info) = verify_user('login', username, password)
            if status == 2:
                error = run_info
                return render_to_response('admin_login.html', {
                    'form':form, 
                    'error':error, 
                    'context':context}
                )
            
            u = {"username":username, "password":password}
            req.session['login'] = u
            return HttpResponseRedirect('/admin')
    else:
        form = manager_login()
    return render_to_response('admin_login.html', {'context':context, 'form':form, 'error':error})
    
