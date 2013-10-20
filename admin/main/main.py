from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from is_login import *

#index page
def index_sc(req, context):
	is_ok = is_manager_login(req, context)
	if is_ok == 0:
		return HttpResponseRedirect('/admin/admin_login/')
	return render_to_response('admin_index.html')

def oj_sc(req, context):
	is_ok = is_manager_login(req, context)
	if is_ok == 0:
		return HttpResponseRedirect('/admin/admin_login/')
	return HttpResponseRedirect('/')
#left menu
def menu_sc(req, context):
	is_ok = is_manager_login(req, context)
	if is_ok == 0:
		return HttpResponseRedirect('/admin/admin_login/')
	return render_to_response('admin_menu.html')

# welcome page
def welcome_sc(req, context):
	is_ok = is_manager_login(req, context)
	if is_ok == 0:
		return HttpResponseRedirect('/admin/admin_login/')
	return render_to_response('welcome.html')
