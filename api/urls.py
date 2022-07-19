from django.urls import include, re_path

from api import views

urlpatterns = [
    re_path(r"^$", views.root, name="root"),
    re_path(r"^annotator/annotations/?$", views.index_create, name="index_create"),
    re_path(r"^annotator/annotations/(?P<pk>.+)/?$", views.read_update_delete, name="read_update_delete"),
    re_path(r"^annotator/search/?$", views.search, name="search"),
    re_path(r"^reader/?$", views.reading_log, name="reading_log"),
    re_path(r"^quiz/?$", views.quiz, name="quiz"),
    re_path(r"^quiz/assess?$", views.assess, name="assess"),
    re_path(r"^quiz/attempt?$", views.attempt, name="attempt"),
    re_path(r"^kcs/?$", views.kcs, name="kcs"),
    re_path(r"^summary/?$", views.summary, name="summary"),
    re_path(r"^recommender/recommended_videos?$", views.recommended_videos, name="recommended_videos"),
    re_path(r"^smart_learning_content/programming?$",views.slc_programming,name="slc"),
    re_path(r"^wiki_resources_content?$",views.wiki_resources_content,name="slc"),
    re_path(r"^knowledgevis/concept_map?$",views.concept_map, name="get_concept_map"),
    re_path(r"^knowledgevis/concept_map_log?$",views.concept_map_log, name="concept_map_log"),
    re_path(r"^reader/assignments?$",views.assignments, name="assignments"),
    re_path(r"^recommender/rate_resource?$", views.rate_resource, name="rate_resource"),
    re_path(r"^recommender/recommendations_ratings?$", views.recommendations_ratings, name="recommendations_ratings")
]
