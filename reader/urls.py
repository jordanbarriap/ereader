from django.urls import include, re_path
from django.contrib import admin
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
        re_path(r'^reader\/(?P<url_course_id>[\d]+)\/(?P<url_section_id>[\w|\W|\d)]+)\/$', views.load_course_with_section_id, name="course"),
        re_path(r'^reader/(?P<url_group_id>[\w]+)/$', views.load_course, name='group'),
        #re_path(r'^reader/(?P<url_course_id>(\d+)/(?P<url_section_id>(.+))/$', views.load_course_with_section_id, name='course_section'),
        re_path(r'^login/$', auth_views.LoginView.as_view(), name='login'),
        re_path(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
        re_path(r'^admin/$', admin.site.urls),
        re_path(r'^home/', views.home, name='user'),
]
