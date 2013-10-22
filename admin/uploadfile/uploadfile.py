#coding=utf-8

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from string import join,split
from django.core.paginator import Paginator
import os, os.path
from oj.models import *
from admin.is_login.is_login import *
from qduoj_config import *
from admin.uploadfile.uploadfile import *

def unzipfiles(proid, files):
	filename = '%s' % files.name
	name, ext = os.path.splitext(filename)
	filedir = r'%s/%s' % (proid, filename)
	targetFile = os.path.join(TEST_DATA_PATH, filedir)
	targetDir = os.path.join(TEST_DATA_PATH, proid)

	print ext + 'hehe'
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
