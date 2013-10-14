from django.contrib import admin
from oj.models import *

class AuthorAdmin(admin.ModelAdmin):
	pass
class ProblemAdmin(admin.ModelAdmin):
	list_display = ['problem_id', 'title', 'content_file']
	ordering = ['problem_id']

admin.site.register(User)
admin.site.register(Problem, ProblemAdmin)
admin.site.register(LoginLog)
admin.site.register(News)
admin.site.register(Solution)
admin.site.register(Source_code)
admin.site.register(Mail)
