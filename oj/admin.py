from django.contrib import admin
from oj.models import *

class AuthorAdmin(admin.ModelAdmin):
	pass

admin.site.register(User)
admin.site.register(Problem)
admin.site.register(LoginLog)
admin.site.register(News)
admin.site.register(Solution)
admin.site.register(Source_code)
admin.site.register(Mail)
admin.site.register(Contest)
admin.site.register(Contest_problem)
admin.site.register(Compileinfo)
admin.site.register(Runtimeinfo)
