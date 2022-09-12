from django.urls import include, re_path
from django.contrib import admin
from . import views

urlpatterns = [
        #re_path(r'^reader/(?P<course_id>[0-9]+)/$', views.load_course, name="course"),
        re_path(r'^/*', views.panel, name='user'),
]
