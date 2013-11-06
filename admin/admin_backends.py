#coding=utf8

from django.http import  HttpResponseRedirect
from functools import wraps

def permission_asked(permission):
    '''
    this decorator verify the user now whether has priorities
    if yes, return the function, else return the login page
    '''
    def wrapper(function):
        @wraps(function)
        def wrapped(req, context, *args, **kwargs):
            if (not 'ojlogin' in context or 
                context['ojlogin'].has_perm(permission) == False):  
                return HttpResponseRedirect('/admin/admin_login')
            else:
                return function(req, context, *args, **kwargs)
        return wrapped
    return wrapper

def is_manager(function):
    '''
    this decorator verify the user now whether is a manager
    if yes, return the function, else return the login page
    '''
    @wraps(function)
    def wrapper(req, context, *args, **kwargs):
        if not 'ojlogin' in context or context['ojlogin'].isManager == False:
            return HttpResponseRedirect('/admin/admin_login')
        else:
            return function(req, context, *args, **kwargs)

    return wrapper

def has_any_perm(function):
    '''
    if one has any perms can login this
    '''
    @wraps(function)
    def wrapper(req, context, *args, **kwargs):
        if (not 'ojlogin' in context or 
            (not context['ojlogin'].get_all_permission 
             and context['ojlogin'].isManager == False)):
            return HttpResponseRedirect('/admin/admin_login')
        else:
            return function(req, context, *args, **kwargs)
    return wrapper
