from django.db.models import JSONField, Model
from django.db import models
from django.contrib.auth.models import User

from django.utils import timezone

# Create your models here.

class WikiConcepts(models.Model):
    id = models.AutoField(primary_key=True)
    resource_id = models.CharField(max_length=200)
    concept = models.CharField(max_length=200)
    wikipage = models.CharField(max_length=200)
    score = models.IntegerField()

    def __str__(self):
        return f"{self.resource_id},{self.concept},{self.wikipage}"

    class Meta:
        app_label="wiki_concepts"
        db_table = "wiki_concepts"

class WikiFeedback(models.Model):
    id = models.AutoField(primary_key=True)
    resource_id = models.CharField(max_length=200)
    concept = models.CharField(max_length=200)
    wiki_article_id = models.IntegerField()
    article_rating = models.IntegerField()
    wiki_feedback = models.CharField(max_length=1000)

    def __str__(self):
        return f"{self.resource_id},{self.concept},{self.wiki_article_id}"

    def is_valid(self):
        return len(self.resource_id)!=0 and len(self.concept) != 0

    class Meta:
        app_label="wiki_feedback"
        db_table = "wiki_feedback"
