# coding=utf-8
from django.shortcuts import render_to_response
from oj.models import User

def verify_user(fun, nick, password):
    '''
    verify user when user is logining or registering
    if verify return 1 login success
    if verify return 0 register success
    '''
    run_info = {}
    user = User.objects.filter(nick=nick)
    if fun == 'login':
        user = user.filter(password = password)
    if len(user) == 0:
        status = 0
        run_info['error'] = 'the user name or the password is wrong'
    elif not user.get_all_permission:
        status = 2
        run_info['error'] = 'the admin is not exists'
    else:
        status = 1
        run_info['error'] = 'the user already exists'
    return (status, run_info)

def error(title, page_info, context):
    '''when requst wrong, return to this page'''
    return render_to_response('error.html', {
        'pageInfo':page_info,
        'title':title, 'context':context}
    )

def jump_page(url, info):
    '''the transit page'''
    return render_to_response('jump.html', {'url':url, 'info':info})

