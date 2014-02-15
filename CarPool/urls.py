from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'CarPool.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'WebUI.views.home'),
    url(r'^save_journey/$', 'WebUI.views.save_journey'),
    url(r'^admin/', include(admin.site.urls)),
)
