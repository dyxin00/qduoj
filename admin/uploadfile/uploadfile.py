#coding=utf-8

import os, os.path
from oj.models import *
from admin.is_login.is_login import *
from oj.qduoj_config.qduoj_config import *
from admin.uploadfile.uploadfile import *

def unzipfiles(proid, files):
    filename = '%s' % files.name
    name, ext = os.path.splitext(filename)
    filedir = r'%s/%s' % (proid, filename)
    targetFile = os.path.join(TEST_DATA_PATH, filedir)
    targetDir = os.path.join(TEST_DATA_PATH, proid)

    if ext == '.zip':
        cmd = r'unzip -o -d %s %s' % (targetDir, targetFile)
        os.system(cmd)
        os.remove(targetFile)
    elif ext == '.tar':
        os.remove(targetFile)
    elif ext == '.rar':
        cmd = r'unrar e -o+ %s %s' % (targetFile, targetDir)
        os.system(cmd)
        os.remove(targetFile)
    
def handle_load_files(proid, files):
    name = r'%s/%s' % (proid, files.name)
    targetDir = os.path.join(TEST_DATA_PATH, name)
    if os.path.isfile(targetDir):
        os.remove(targetDir)
    destination = open(targetDir, 'w')
    for chunk in files.chunks():
        destination.write(chunk)
    destination.close()
    unzipfiles(proid, files)

def remove_file_folder(req, targetFile):
    if os.path.isfile(targetFile):
        os.remove(targetFile)
    elif os.path.isdir(targetFile):
        for item in os.listdir(targetFile):
            src = os.path.join(targetFile, item)
            remove_file_folder(req, src)
        os.rmdir(targetFile)    

def is_file_exists(req, proid, filename):
    name = r'%s/%s' % (proid, filename)
    targetFile = os.path.join(TEST_DATA_PATH, name)
    print targetFile
    if os.path.isfile(targetFile):
        return (targetFile, 2)
    elif os.path.isdir(targetFile):
        return (targetFile, 1)
    else:
        return (targetFile, 0)

def downfile_via_url(req, targetDir, filename):
    files = open(targetDir)
    data = files.read()
    files.close()
    response = HttpResponse(data, mimetype='application/ontet-stream')
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response

