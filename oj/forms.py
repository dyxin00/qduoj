#coding=utf8
from django import forms
from django.forms import ModelForm
from oj.models import User

class Login(forms.Form):
    name = forms.CharField(label='用户')
    password = forms.CharField(label='密码', widget=forms.PasswordInput)

class Register(ModelForm):
    '''use User model create the register model'''
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('nick', 'password', 'email', 'website')

class Submit_code(forms.Form):
    language = forms.ChoiceField(choices = [('0','c'),('1','c++')])
    submit_code = forms.CharField(label='code',widget=forms.Textarea(attrs={'class':'submit','cols':'120','style':'width:70%','rows' : '20'}))

class Send_mail(forms.Form):
    send_to = forms.CharField(max_length=20)
    title = forms.CharField(max_length=50)
    content = forms.CharField(label='mail',widget=forms.Textarea(attrs={'class':'submit','cols':'120','style':'width:40%','rows' : '20'}))

    
class ChangePw(forms.Form):
    pw_current = forms.CharField(widget = forms.PasswordInput)
    pw_now = forms.CharField(widget = forms.PasswordInput)
    ensure_pw = forms.CharField(widget = forms.PasswordInput)

class Classification(forms.Form):
    choices = [('0','全部'),
               ('1','模拟'),
               ('2','动态规划'),
               ('3','字符串处理'),
               ('4','搜索'),
               ('5','数论'),
               ('6','计算几何'),
               ('7','图论'),
               ('8','树结构'),
               ('9','并查集'),
               ('10','贪心'),
               ('11','网络流'),
               ('12','博弈')
              ]
    classification  = forms.ChoiceField(choices = choices)

