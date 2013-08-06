from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/?', include(admin.site.urls)),
    url(r'^setuser/(?P<userid>[-\d]+)/?$', 'food.views.home'),
    url(r'^chooseplace/(?P<placeid>[-\d]+)/?$', 'food.views.chooseplace'),
    url(r'^signout/?', 'food.views.signout'),
    url(r'^$', 'food.views.home', name='home'),
)
