#coding=utf-8

'''this contains the user login and register!'''
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from oj.forms import Login, Register
from oj.tools import verify_user, jump_page

def login_sc(req, context):
    error = {}
    if req.method == 'POST':
        form = Login(req.POST)
        if form.is_valid():
            username = form.cleaned_data['name']
            password = form.cleaned_data['password']
            (status, run_info) = verify_user('login', username, password)
            if status == 0:
               error = run_info
               return render_to_response('login.html', {
                    'form':form, 
                    'error':error, 
                    'context':context}
                )   
            u = {"username":username, "password":password}
            req.session['login'] = u
            return HttpResponseRedirect(req.session['login_from'])
    else:
        form = Login()
        req.session['login_from'] = req.META.get('HTTP_REFERER', '/')
    return render_to_response('login.html', {
        'form':form, 
        'error':error, 
        'context':context}
    )

def register_sc(req, context):
    error = {}
    if req.method == "POST":
        form = Register(req.POST)
        if form.is_valid():
            user = form.save(commit = False)
            (status, run_info) = verify_user('register', user.nick, '')
            print run_info
            if status == 1: #status 1 user all ready exist
                error = run_info
            else:
                user.save()
                #first para repreasent the url, second the info of jump page
                return jump_page('/', 'register success')
    else:
        form = Register()
    return render_to_response('register.html', {'form':form, 'error':error, 'context':context})

def logout_sc(req):
    del req.session['login']
    return jump_page('/', 'logout success')

