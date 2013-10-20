#coding=utf8
from  django import forms

class Login(forms.Form):
	name = forms.CharField(label='用户')
	password = forms.CharField(label='密码', widget=forms.PasswordInput)

class Register(forms.Form):
	name = forms.CharField(label='用户名')
	password = forms.CharField(label='输入密码', widget=forms.PasswordInput)
	ensure_pw = forms.CharField(label='确认密码', widget=forms.PasswordInput)
	email = forms.EmailField(label='Email')
	website = forms.URLField(label='website', required=False)

class Submit_code(forms.Form):
	language = forms.ChoiceField(choices = [('0','c'),('1','c++')])
	submit_code = forms.CharField(label='code',widget=forms.Textarea(attrs={'class':'submit','cols':'120','style':'width:70%','rows' : '20'}))

class Send_mail(forms.Form):
	send_to = forms.CharField(max_length=20)
	title = forms.CharField(max_length=50)
	content = forms.CharField(label='mail',widget=forms.Textarea(attrs={'class':'submit','cols':'120','style':'width:40%','rows' : '20'}))

class Status(forms.Form):
	Result_choices = [
			('-1','All'),
			('4','AC'),
			('5','PE'),
			('6','WA'),
			('7','TLE'),
			('8','MLE'),
			('9','OLE'),
			('10','RE'),
			('11','CE'),
			('0','PD'),
			('1','PR'),
			('2','CI'),
			('3','RJ'),
			]
	#problem_id = forms.CharField(attrs={'class':'input-mini','style':'height:24px','size': '4'})
	problem_id = forms.CharField(max_length=20)
	user = forms.CharField()
	language = forms.ChoiceField(choices = [('-1','All'),('0','c'),('1','c++')])
	result = forms.ChoiceField(choices = Result_choices)
	
class ChangePw(forms.Form):
	pw_current = forms.CharField(widget = forms.PasswordInput)
	pw_now = forms.CharField(widget = forms.PasswordInput)
	ensure_pw = forms.CharField(widget = forms.PasswordInput)
