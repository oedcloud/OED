from django.conf.urls.defaults import patterns, include, url
#from hosts.views import ospcdeploy
import settings
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^ospcdeploy/$','hosts.views.ospcdeploy'),
    (r'^getlog/$','hosts.views.getlog'),
    (r'^logger/','hosts.views.clientlog'),
    # Examples:
    # url(r'^$', 'ospcdeploy.views.home', name='home'),
    # url(r'^ospcdeploy/', include('ospcdeploy.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
