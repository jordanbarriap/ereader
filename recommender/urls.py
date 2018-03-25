from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
        #url(r'^reader/(?P<course_id>[0-9]+)/$', views.load_course, name="course"),
        url(r'^/*', views.panel, name='user'),
]