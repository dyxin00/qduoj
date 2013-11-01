#coding=utf-8

'''change the base info of the user'''
from django.shortcuts import render_to_response
from oj.models import User
from oj.forms import ChangePw
from oj.util.util import login_asked
from oj.tools import jump_page

@login_asked
def changepw_sc(req, context):
    '''change the password of the user'''
    error = {}
    if req.method == 'POST':
        form = ChangePw(req.POST)
        if form.is_valid():
            pw_current = form.cleaned_data['pw_current']
            user = User.objects.filter(nick=context['ojlogin'].nick)
            if user[0].password == pw_current:
                pw_now = form.cleaned_data['pw_now']
                user.update(password=pw_now)
                url = '/user_info/name='+user[0].nick
                return jump_page(url, 'change success')
            else:
                error_info = "you enter the wrong password!"
                error['error'] = error_info
    else:
        form = ChangePw()
    return render_to_response('changepw.html', {
        'context':context,
        'form':form,
        'error':error}
    )

@login_asked
def changeinfo_sc(req, context):
    '''change the mail or the website of the user'''
    user = User.objects.filter(nick=context['ojlogin'].nick)
    
    if req.method == 'POST':
        Email = req.POST['email']
        Website = req.POST['website']
        user.update(email=Email)
        user.update(website=Website)
        url = '/user_info/name='+user[0].nick
        return jump_page(url, 'change success')
    
    return render_to_response('changeinfo.html', {
        'user':user[0],
        'context':context}
    )
