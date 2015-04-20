from django.conf.urls import patterns, include, url
from django.contrib import admin
from app.views import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Znajdz_Mi_Kino.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', index, name='index'),
    url(r'^map/$', mapa, name='mapa'),
    url(r'^repertuar/kino/(?P<cinema>\d+)/0/$', by_cinema, name='by_cinema'),
    url(r'^repertuar/kino/(?P<cinema>\d+)/(?P<day>[012])/$', by_cinema, name='by_cinema'),
    url(r'^repertuar/film/(?P<movie>\d+)/0/$', by_movie, name='by_movie'),
    url(r'^repertuar/film/(?P<movie>\d+)/(?P<day>[012])/$', by_movie, name='by_movie'),
    url(r'^repertuar/0/$', repertuar, name='repertuar'),
    url(r'^repertuar/(?P<day>[012])/$', repertuar, name='repertuar'),
    url(r'^import/$', data_import),

)
