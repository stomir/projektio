from django.conf.urls import patterns, include, url
from django.contrib import admin
from app.views import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Znajdz_Mi_Kino.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^$', index, name='index'),
    url(r'^map/$', mapa, name='mapa'),
    url(r'^repertuar/(?P<c_type>[\w+%-]*)/(?P<what>[\w+%-]*)/$', repertuar, name='repertuar'),
    url(r'^import/$', data_import),

)
