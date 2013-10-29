from django import forms
from django.forms import ModelForm
from oj.models import Problem, News, Perm

class manager_login(forms.Form):
    '''the form appears when the manager is not login'''
    name = forms.CharField(max_length=30)
    password = forms.CharField(widget = forms.PasswordInput)

class ProblemSearch(forms.Form):
    '''
    when manage the problem, using it,
    can search some problem quickly via id
    '''
    search_id = forms.DecimalField()

class Admin_UploadFiles(forms.Form):
    '''
    after the adding problems this can load files
    for problem
    '''
    files = forms.FileField(widget=forms.FileInput) 

class NewsForm(ModelForm):
    '''
    news form fun:
    edit News
    add news 
     '''
    class Meta:
        model = News
        fields = (
            'title',
            'content'
        )

class ProblemForm(ModelForm):
    '''
    problem form fun:
    edit problem 
    add problem
    '''
    class Meta:
        model = Problem
        fields = ('title', 'time_limit', 'memory_limit',
                  'hard', 'description', 'input_data', 
                  'sample_input', 'sample_output', 'output_data',
                  'source', 'hint'
                 )

class AdminSearch(forms.Form):
    '''this is the form '''
    nick = forms.CharField(max_length = 50)

