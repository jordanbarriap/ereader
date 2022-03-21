from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
        url(r'^reader\/(?P<url_course_id>[\d]+)\/(?P<url_section_id>[\w|\W|\d)]+)\/$', views.load_course_with_section_id, name="course"),
        url(r'^reader/(?P<url_group_id>[\w]+)/$', views.load_course, name='group'),
        #url(r'^reader/(?P<url_course_id>(\d+)/(?P<url_section_id>(.+))/$', views.load_course_with_section_id, name='course_section'),
        url(r'^login/$', auth_views.login, name='login'),
        url(r'^logout/$', auth_views.logout, name='logout'),
        url(r'^admin/$', admin.site.urls),
        url(r'^home/', views.home, name='user'),
]