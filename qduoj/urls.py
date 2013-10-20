from django.conf.urls import patterns, include, url

#Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'qduoj.views.home', name='home'),
    # url(r'^qduoj/', include('qduoj.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
	url('^$', 'oj.views.problemlist'),  # the init page is one
	url('^oj/$', 'oj.views.problemlist'),
	url('problemlist/page=(?P<page>\d+)/$', 'oj.views.problemlist'),#through the num to shift page 
	url('^problem/num=(?P<num>\d+)/$', 'oj.views.problem'),
	url('^oj/userlogin/$', 'oj.views.login'),                      #log
	url('^oj/userregister/$', 'oj.views.register'),				   #register
	url('^oj/userlogout/$', 'oj.views.logout'),                    #logout
	#url(r'^admin/', include(admin.site.urls)),
	url('^problemid/$','oj.views.problemId'),
	url('^problem_search/$','oj.views.problem_search'),
	url(r'^rank/$', 'oj.views.rank'),
	url(r'^rank/page=(?P<page>\d+)/$', 'oj.views.rank'),
	url(r'^user_info/name=(?P<nick>\w+)/$', 'oj.views.user_info'),
	url('^submit_code/num=(?P<num>\d+)/$', 'oj.views.submit_code'),

	url('^status/$','oj.views.status'),
	url('^status/page=(?P<page>\d+)/$', 'oj.views.status'),
	url('^Search_status/$','oj.views.status_Search'),
	url('^Search_status/page=(?P<page>\d+>)/$', 'oj.views.status_Search'),
	
	url('^source_code/runid=(?P<runid>\d+)/$', 'oj.views.source_code'),
	url('^changepw/$', 'oj.views.changepw'),
	url('^changeinfo/$', 'oj.views.changeinfo'),
	
	url('^mail/$', 'oj.views.mail'),
	url('^mail/pattern=(?P<fun>\d+)/$', 'oj.views.mail'),
	url('^readmail/pattern=(?P<fun>\d+)/msgid=(?P<msgid>\d+)/$', 'oj.views.readmail'),
	
#	url('^bbs/pid=(?P<pid>\d+)\$', 'oj.views.bbs'),
#	url('^bbs/pid=(?P<pid>\d+)/page=(?<page>\d+)\$', 'oj.views.bbs'),
)

urlpatterns += patterns('',
	url('^admin/$', 'admin.views.index'),
	#url('^admin/oj$', 'admin.views.oj'),
	url('^admin/welcome/$', 'admin.views.welcome'),
	url('^admin/menu/$', 'admin.views.menu'),
	url('^admin/admin_login/$', 'admin.views.admin_login'),
	url('^admin/news_list/$', 'admin.views.news'),
	url('^admin/add_news/$', 'admin.views.add_news'),
	url('^admin/edit_news/msgid=(?P<msgid>\d+)/$', 'admin.views.edit_news'),
	url('^admin/news_visible/msgid=(?P<msgid>\d+)/$', 'admin.views.news_visible'),
	url('^admin/problem_list/$', 'admin.views.problem_list'),
	url('^admin/problem_list/page=(?P<page>\d+)/$', 'admin.views.problem_list'),
	url('^admin/add_problem/$', 'admin.views.add_problem'),
	url('^admin/pro_search/$', 'admin.views.admin_search'),
)
