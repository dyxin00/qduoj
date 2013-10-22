from django import forms

class manager_login(forms.Form):
	name = forms.CharField()
	password = forms.CharField(widget = forms.PasswordInput)
