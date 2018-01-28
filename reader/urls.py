from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
        #url(r'^reader/(?P<course_id>[0-9]+)/$', views.load_course, name="course"),
        url(r'^reader/(?P<url_group_id>[\w]+)/$', views.load_course, name='group'),
        url(r'^login/$', auth_views.login, name='login'),
        url(r'^logout/$', auth_views.logout, name='logout'),
        url(r'^admin/', admin.site.urls),
        url(r'^home/', views.home, name='user'),
]