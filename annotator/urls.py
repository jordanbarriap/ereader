from django.urls import include, re_path

from annotator import views

urlpatterns = [
    re_path(r"^$", views.root, name="root"),
    re_path(r"^annotations/?$", views.index_create, name="index_create"),
    re_path(r"^annotations/(?P<pk>.+)/?$", views.read_update_delete, name="read_update_delete"),
    re_path(r"^search/?$", views.search, name="search"),
]
