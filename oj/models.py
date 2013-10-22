from django.db import models
import os
from qduoj import settings

class Contest(models.Model):
	contest_id = models.AutoField(primary_key=True)
	title = models.CharField(max_length = 50)
	start_time = models.DateTimeField()
	end__time = models.DateTimeField()
	defunct = models.BooleanField(default = True)
	private = models.BooleanField(default = True)
	oi_mode = models.BooleanField(default = False)
	def __unicode__(self):
		return str(self.contest_id) + ' - ' + self.title
class Contest_problem(models.Model):
	problem_id = models.IntegerField(default=0)
	contest_id = models.IntegerField(default=0)
	title = models.CharField(max_length = 50)
	num = models.IntegerField(default = 0)
	score = models.IntegerField(default = 100)
	def __unicode__(self):
		return 'contest_id - '+  str(self.contest_id) + ' - ' + self.title

class User(models.Model):	
	user_id = models.AutoField(primary_key=True)
	nick = models.CharField(max_length=50)
	password = models.CharField(max_length=100)
	email = models.EmailField(null=True, blank=True)
	isManager = models.IntegerField(default=0)
	website = models.CharField(max_length=50)
	ac = models.IntegerField(default=0)
	submit = models.IntegerField(default=0)
	rank = models.IntegerField(default=0)

	def __unicode__(self):
		return self.nick

class Problem(models.Model):
#	def get_file_upload_to(instance, filename):
#		print "hehea"
#		return	str(instance.problem_id)+ "/" + filename
	problem_id = models.AutoField(primary_key=True)
	title = models.CharField(max_length=50)
	description = models.TextField()
	input_data = models.TextField()
	output_data = models.TextField()
	sample_input = models.TextField()
	sameple_output = models.TextField()
	source = models.CharField(max_length=50, null=True, blank=True)
	hint = models.TextField(null=True, blank=True)
	in_date = models.DateTimeField(auto_now_add=True)
	time_limit = models.IntegerField()
	memory_limit = models.IntegerField()
	hard = models.IntegerField()
	accepted = models.IntegerField(default=0)
	submit = models.IntegerField(default=0)
	visible = models.BooleanField(default=True)
	oi_mode = models.BooleanField(default=False)
	#content_file = models.FileField(upload_to=get_file_upload_to)
	def __unicode__(self):
		return str(self.problem_id) + ":  " + self.title

#	post_delete.connect(delete_file, sender=Problem)
class Solution(models.Model):
	solution_id = models.AutoField(primary_key=True)
	problem = models.ForeignKey(Problem)
	user = models.ForeignKey(User)
	contest_id = models.IntegerField(default=-1)
	score = models.FloatField(default=0)
	time = models.IntegerField(default=0)
	memory = models.IntegerField(default=0) # ...
	in_date = models.DateTimeField(auto_now_add=True)
	result = models.IntegerField(default=0)
	language = models.IntegerField(default=0)
	judgetime = models.DateTimeField(auto_now_add=True)
	code_length = models.IntegerField(default=0)
	def __unicode__(self):
		return str(self.solution_id)

class Source_code(models.Model):
	solution_id = models.IntegerField(primary_key=True)
	code = models.TextField()
	
	def __unicode__(self):
		return str(self.solution_id)

class Compileinfo(models.Model):
	solution_id = models.IntegerField(primary_key=True)
	error = models.TextField()
	
	def __unicode__(self):
		return str(self.solution_id)

class LoginLog(models.Model):
	user = models.ForeignKey('User')
	ip = models.IPAddressField()
	time = models.DateTimeField(auto_now_add=True)
	
	def __unicode__(self):
		return self.user.nick

class News(models.Model):
	title = models.TextField()
	content = models.TextField()
	time = models.DateTimeField(auto_now_add=True)
	visible = models.BooleanField(default=True)
	def __unicode__(self):
		return self.title

class Mail(models.Model):
	mail_id = models.AutoField(primary_key=True)
	mail_to = models.CharField(max_length=50)
	mail_from = models.CharField(max_length=50)
	title = models.TextField()
	content = models.TextField()
	is_new = models.BooleanField(default=False)
	in_date = models.DateTimeField(auto_now_add=True)
	reply = models.CharField(max_length=20, null=True, blank=True)

	def __unicode__(self):
		return str(self.mail_id)

class Bbs(models.Model):
	problem = models.ForeignKey('Problem')
	user = models.ForeignKey('User')
	time = models.DateTimeField(auto_now_add=True)	
	text = models.TextField()
	reply_id = models.IntegerField() #if the id == 0, this reply is to the LZ, else to the flaw
	stairs = models.IntegerField()

	def __unicode__(self):
		return str(self.problem.problem_id)

class Runtimeinfo(models.Model):
	solution_id = models.IntegerField(primary_key=True)
	error = models.TextField()

	def __unicode__(self):
		return str(self.solution_id)
