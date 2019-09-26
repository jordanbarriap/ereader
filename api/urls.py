from django.conf.urls import include, url

from api import views

urlpatterns = [
    url(r"^$", views.root, name="root"),
    url(r"^annotator/annotations/?$", views.index_create, name="index_create"),
    url(r"^annotator/annotations/(?P<pk>.+)/?$", views.read_update_delete, name="read_update_delete"),
    url(r"^annotator/search/?$", views.search, name="search"),
    url(r"^reader/?$", views.reading_log, name="reading_log"),
    url(r"^quiz/?$", views.quiz, name="quiz"),
    url(r"^quiz/assess?$", views.assess, name="assess"),
    url(r"^quiz/attempt?$", views.attempt, name="attempt"),
    url(r"^kcs/?$", views.kcs, name="kcs"),
    url(r"^summary/?$", views.summary, name="summary"),
    url(r"^recommender/recommended_videos?$", views.recommended_videos, name="recommended_videos"),
    url(r"^knowledgevis/concept_map?$",views.concept_map, name="get_concept_map"),
    url(r"^knowledgevis/concept_map_log?$",views.concept_map_log, name="concept_map_log"),
    url(r"^reader/assignments?$",views.assignments, name="assignments"),
    url(r"^recommender/rate_resource?$", views.rate_resource, name="rate_resource"),
    url(r"^recommender/recommendations_ratings?$", views.recommendations_ratings, name="recommendations_ratings")
]