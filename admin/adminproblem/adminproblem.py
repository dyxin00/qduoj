#coding=utf-8

from django.shortcuts import render_to_response
import os, os.path
from oj.models import Problem 
from oj.qduoj_config.qduoj_config import ADMIN_PAGE_PROBLEM_NUM
from oj.util.util import paging
from admin.uploadfile.uploadfile import *
from admin.admin_backends import permission_asked
from admin.forms import ProblemSearch, Admin_UploadFiles
from admin.forms import ProblemForm
from oj.tools import error

@permission_asked('problem_add')
def admin_problem_list_sc(req, context, page):
    page = int(page)
    if ('minisiter' in context['ojlogin'].get_all_permission
        or context['ojlogin'].isManager == True):
        problem =  Problem.objects.order_by('problem_id')
    else:    
        problem = Problem.objects.filter(provider_id=context['ojlogin'].user_id).order_by('problem_id')
    (problemset, list_info) = paging(problem, ADMIN_PAGE_PROBLEM_NUM, page)
    permlist = context['ojlogin'].get_all_permission
    #if the requst is out of bound, error!
    if problemset == None: 
        return error('404', 'page not found', context, 'admin_error.html');
    if req.method == 'POST':
        form = ProblemSearch(req.POST)
        if form.is_valid():
            proid = form.cleaned_data['search_id']
            problem = Problem.objects.filter(problem_id=proid)
            problem = problem.filter(provider_id=context['ojlogin'].user_id)
            return render_to_response('admin_problem_list.html', {
                'problems':problem, 'permlist':permlist, 'context':context}
            )
    else:
        form = ProblemSearch()
    return render_to_response('admin_problem_list.html', {
        'problems':problemset,
        'context':context, 
        'list_info':list_info, 
        'form':form,
        'permlist':permlist,
        }
    )
@permission_asked('problem_add')
def admin_add_problem_sc(req, context):
    if req.method == 'POST':
        form = ProblemForm(req.POST)
        if form.is_valid():
            problem = form.save(commit=False)
            problem.provider_id = context['ojlogin'].user_id # this saves the author of it
            problem.save()
            return HttpResponseRedirect(
                '/admin/if_add_data/proid=%s'%problem.problem_id
                )
    else:
        form = ProblemForm()
    return render_to_response('admin_add_problem.html', {
        'context':context, 
        'form':form}
    )

@permission_asked('problem_add')
def admin_edit_problem_sc(req, context, proid):
    problem = Problem.objects.filter(problem_id=proid)
    if len(problem) == 0:
        return error('404', 'page not found', context, 'admin_error.html')
    if req.method == 'POST':
        form = ProblemForm(req.POST, instance = problem[0])
        if form.is_valid():
            form.save()    
            return HttpResponseRedirect(
                '/admin/problem_list'
                )
    else:
        form = ProblemForm(instance=problem[0])
    return render_to_response('admin_edit_problem.html', {
        'form':form, 
        'context':context}
    )

@permission_asked('problem_add')
def problem_shift_mode_sc(req, context, proid, page, fun):
    problem = Problem.objects.filter(problem_id=proid)
    permlist = context['ojlogin'].get_all_permission
    if len(problem) == 0:
        return error('404', 'no this problem', context, 'admin_error.html')
    if fun == 'visible':
        if problem[0].visible == True:
            problem.update(visible=False)
        else:
            problem.update(visible=True)
    elif fun == 'oi_mode':
        if problem[0].oi_mode == True:
            problem.update(oi_mode=False)
        else:
            problem.update(oi_mode=True)
    if page == '0':
        problem = Problem.objects.filter(problem_id=proid)
        return render_to_response('admin_problem_list.html', {
            'problems': problem, 'permlist':permlist}
        )
    else:
        return HttpResponseRedirect(
            '/admin/problem_list/page=%s' % page
            )


@permission_asked('problem_add')
def if_add_data_sc(req, context, proid):
    targetDir = os.path.join(TEST_DATA_PATH, proid)
    if not os.path.exists(targetDir):
        os.makedirs(targetDir)
    problem = Problem.objects.filter(problem_id = proid)
    return render_to_response('admin_if_add_data.html', {
        'problem':problem[0]}
    )

@permission_asked('problem_add')
def problem_testdata_sc(req, context, proid):
    targetDir = os.path.join(TEST_DATA_PATH, proid)
    try:
        files = os.listdir(targetDir)
    except IOError:
        pageInfo = 'the problem %s not exist' % proid
        return render_to_response('admin_error.html', {
            'pageInfo':pageInfo}
        )
    if req.method == 'POST':
        form = Admin_UploadFiles(req.POST, req.FILES)
        if form.is_valid():
            files = req.FILES['files']
            if files.size <= MAX_UPLOAD_FILE_SIZE * 1000000:
                handle_load_files(proid, req.FILES['files']) #error
                files = os.listdir(targetDir)
                return render_to_response('problem_filelist.html', {
                    'files':files, 
                    'proid':proid, 
                    'form':form}
                ) 
            else:
                pageInfo = 'the file size exceed the max size 5M'   
                return render_to_response('admin_error.html', {
                    'pageInfo':pageInfo}
                )
    else:
        form = Admin_UploadFiles()
    return render_to_response('problem_filelist.html', {
        'files':files,
        'proid':proid,
        'form':form}
    )

@permission_asked('problem_add')
def delete_testdata_sc(req, context, proid, filename):
    (targetFile, is_file) = is_file_exists(req, proid, filename)
    if is_file == 0:
        pageInfo = 'the file %s not exist' % filename
        return render_to_response('admin_error.html', {
            'pageInfo':pageInfo}
        )
    elif is_file == 1: #if 1, it is a file folder
        remove_file_folder(req, targetFile)
    else:
        os.remove(targetFile)
    return HttpResponseRedirect(
        '/admin/problem_testdata/proid=%s'%proid
        )

@permission_asked('problem_add')
def download_testfile_sc(req, context, proid, filename):
    (targetFile, is_file) = is_file_exists(req, proid, filename)
    if is_file == 0 or is_file == 1:
        pageInfo = 'the file %s is a folder or not exist' % filename
        return render_to_response('admin_error.html', {
            'pageInfo':pageInfo}
        )
    return downfile_via_url(req, targetFile, filename)
    
