from django.conf.urls import patterns, include, url
from django.contrib.sitemaps import views as sitemap_views
from django.views.decorators.cache import cache_page
from oj.sitemap import PostSitemap
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
    url('^sitemap\.xml$', cache_page(sitemap_views.sitemap, 60 * 60 * 12), {'sitemaps':{'posts':PostSitemap}}),
	url('problemlist/page=(?P<page>\d+)/$', 'oj.views.problemlist'),#through the num to shift page 
	url('^problem/num=(?P<num>\d+)/$', 'oj.views.problem'),
	url('^problem/num=(?P<num>\d+)/cid=(?P<cid>\d+)/$', 'oj.views.contest_problem'),

	url('^oj/userlogin/$', 'oj.views.login'),                      #log
	url('^oj/userregister/$', 'oj.views.register'),				   #register
	url('^oj/userlogout/$', 'oj.views.logout'),                    #logout

#	url(r'^admin/', include(admin.site.urls)),

	url('^problemid/$','oj.views.problemid'),
	url('^problem_search/$','oj.views.problem_search'),

	url(r'^rank/$', 'oj.views.rank'),
	url(r'^rank/page=(?P<page>\d+)/$', 'oj.views.rank'),
	url(r'^user_info/name=(?P<nick>\w+)/$', 'oj.views.user_info'),

	url('^submit_code/num=(?P<num>\d+)/$', 'oj.views.submit_code'),
	url('^submit_code/num=(?P<num>\d+)/cid=(?P<cid>\d+)/$', 'oj.views.contest_submit_code'),

	url('^status/$','oj.views.status'),
	url('^status/page=(?P<page>\d+)/$', 'oj.views.status'),
	url('^Search_status/$','oj.views.status_search'),
	url('^Search_status/page=(?P<page>\d+)/$', 'oj.views.status_search'),
	
	url('^source_code/runid=(?P<runid>\d+)/$', 'oj.views.source_code'),

	url('^changepw/$', 'oj.views.changepw'),
	url('^changeinfo/$', 'oj.views.changeinfo'),
	
	url('^mail/$', 'oj.views.mail'),
	url('^mail/pattern=(?P<fun>\d+)/$', 'oj.views.mail'),
	url('^readmail/pattern=(?P<fun>\d+)/msgid=(?P<msgid>\d+)/$', 'oj.views.readmail'),

	url('^contest_list/$', 'oj.views.contest_list'),
	url('^contest_list/page=(?P<page>\d+)/$', 'oj.views.contest_list'),
	url('^contest/$', 'oj.views.contest'),
	url('^contest/cid=(?P<cid>\d+)/$', 'oj.views.contest'),
	url('^contest_status/cid=(?P<cid>\d+)/$', 'oj.views.contest_status'),
	url('^contest_status/cid=(?P<cid>\d+)/page=(?P<page>\d+)/$', 'oj.views.contest_status'),
	url('^contest_rank/cid=(?P<cid>\d+)/$', 'oj.views.contest_rank'),
	url('^contest_search_status/cid=(?P<cid>\d+)/$','oj.views.contest_status_search'),
	url('^contest_search_status/cid=(?P<cid>\d+)/page=(?P<page>\d+)/$','oj.views.contest_status_search'),
	url('^contest_rank_xls/cid=(?P<cid>\d+)/$','oj.views.contest_rank_xls'),



	url('^compile_error/num=(?P<num>\d+)/$', 'oj.views.compile_error'),
	url('^runtime_error/num=(?P<num>\d+)/$', 'oj.views.runtime_error'),


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
	url('admin/edit_problem/proid=(?P<proid>\d+)/$', 'admin.views.admin_edit_problem'),
	url('admin/problem_shift_mode/proid=(?P<proid>\d+)/page=(?P<page>\d+)/mode=(?P<fun>\w+)/$', 'admin.views.problem_shift_mode'),
	#url('admin/problem_oi_mode/proid=(?P<proid>\d+)/page=(?P<page>\d+)/$', 'admin.views.problem_oi_mode'),
	url('^admin/problem_testdata/proid=(?P<proid>\d+)/$', 'admin.views.problem_testdata'),
	url('^admin/if_add_data/proid=(?P<proid>\d+)/$', 'admin.views.if_add_data'),
	url('^admin/delete_testdata/proid=(?P<proid>\d+)/filename=(?P<filename>[\w.]+)/$', 'admin.views.delete_testdata'),
    url('^admin/down_files/proid=(?P<proid>\d+)/filename=(?P<filename>[\w.]+)/$', 'admin.views.download_testfile'),
    url('^admin/admin_list/$', 'admin.views.admin_list'),
    url('^admin/set_priority/id=(?P<nick>[\w]+)/$', 'admin.views.set_priority'),
    url('^admin/rejudge/$', 'admin.views.rejudge'),
    url('^admin/contest_list/$', 'admin.views.contest_list'),
    url('^admin/contest_list/page=(?P<page>\d+)/$', 'admin.views.contest_list'),  
    url('^admin/contest_shift_mode/conid=(?P<conid>\d+)/page=(?P<page>\d+)/mode=(?P<fun>\w+)/$',
       'admin.views.contest_shift_mode'
       ),
    )
