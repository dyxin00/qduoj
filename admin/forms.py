from django import forms

class manager_login(forms.Form):
    name = forms.CharField(max_length=30)
    password = forms.CharField(widget = forms.PasswordInput)

class admin_news(forms.Form):
    title = forms.CharField(max_length=50)
    content = forms.CharField(label = 'news',widget=forms.Textarea(attrs={'class':'submit','cols':'50','style':'width 40%', 'rows':'10'}))

class admin_problem(forms.Form):
    title = forms.CharField(max_length=50)
    time_limit = forms.DecimalField()
    memory_limit = forms.DecimalField()
    hard = forms.DecimalField()
    description = forms.CharField(widget=forms.Textarea(attrs={'class':'submit', 'cols':'50', 'style':'width 40%', 'rows':'10'}))
    input_data = forms.CharField(widget=forms.Textarea(attrs={'class':'submit', 'cols':'50', 'style':'width 40%', 'rows':'10'}))
    output_data = forms.CharField(widget=forms.Textarea(attrs={'class':'submit', 'cols':'50', 'style':'width 40%', 'rows':'10'}))
    sample_input = forms.CharField(widget=forms.Textarea(attrs={'class':'submit', 'cols':'50', 'style':'width 40%', 'rows':'10'}))
    sample_output = forms.CharField(widget=forms.Textarea(attrs={'class':'submit', 'cols':'50', 'style':'width 40%', 'rows':'10'}))
    source = forms.CharField(max_length=50, required=False)
    hint = forms.CharField(widget=forms.Textarea(attrs={'class':'submit', 'cols':'50', 'style':'width 40%', 'rows':'10'}), required=False)

class adminsearch(forms.Form):
    search_id = forms.DecimalField()

class Admin_UploadFiles(forms.Form):
    files = forms.FileField(widget=forms.FileInput) 
