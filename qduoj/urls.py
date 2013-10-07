from django.conf.urls import patterns, include, url

#Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'qduoj.views.home', name='home'),
    # url(r'^qduoj/', include('qduoj.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
	url('^$', 'oj.views.problemlist'),  # the init page is one
	url('^oj/$', 'oj.views.problemlist'),
	url('problemlist/page=(?P<num>\d+)/$', 'oj.views.problemlist'),#through the num to shift page 
	url('^problem/num=(?P<num>\d+)/$', 'oj.views.problem'),
	url('^oj/userlogin/$', 'oj.views.login'),                      #log
	url('^oj/userregister/$', 'oj.views.register'),				   #register
	url('^oj/userlogout/$', 'oj.views.logout'),                    #logout
	url(r'^admin/', include(admin.site.urls)),
	url('^problemid','oj.views.problemId'),
	url('^problem_search','oj.views.problem_search'),
	url(r'^rank/$', 'oj.views.rank'),
	url('^submit_code/num=(?P<num>\d+)/$', 'oj.views.submit_code'),
)
