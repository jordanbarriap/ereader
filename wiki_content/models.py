from django.db.models import JSONField, Model
from django.db import models
from django.contrib.auth.models import User

from django.utils import timezone

# Create your models here.

class WikiConcepts(models.Model):
    id = models.AutoField(primary_key=True)
    concept = models.CharField(max_length=200)
    tf = models.IntegerField()
    duplicates = models.CharField(max_length=200)
    sim_score = models.FloatField()
    db_link_score = models.FloatField()
    wikipage = models.CharField(max_length=200)
    types = models.CharField(max_length=200)
    overall_score = models.FloatField()
    dbpedia_url = models.CharField(max_length=200)
    is_filtered = models.IntegerField()
    reason_score = models.FloatField()
    reason_type = models.CharField(max_length=200)
    resource_id = models.CharField(max_length=200)
    reason_link = models.CharField(max_length=200)
    is_active = models.IntegerField()
    date_created = models.DateTimeField()
    update_date = models.DateTimeField()
    owner = models.CharField(max_length=200)
    update_action = models.CharField(max_length=200)
    change_field = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.resource_id},{self.concept},{self.wikipage}"

    class Meta:
        app_label="wiki_concepts"
        db_table = "wiki_concepts"

class WikiFeedback(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=200)
    group_id = models.CharField(max_length=200)
    date_added = models.DateTimeField()
    resource_id = models.CharField(max_length=200)
    concept = models.CharField(max_length=200)
    wiki_article_id = models.IntegerField()
    relevance_rating = models.IntegerField()
    difficulty_rating = models.IntegerField()
    # concept_type = models.IntegerField()  -- prerequisite or explained checkbox
    action_type = models.CharField(max_length=200)
    # rec_concepts = models.CharField(max_length=1000) -- student's recommended concept list

    def __str__(self):
        return f"{self.resource_id},{self.concept},{self.wiki_article_id}"

    def is_valid(self):
        return len(self.user_id) != 0 and len(self.group_id) != 0 and len(self.resource_id)!=0 and len(self.concept) != 0

    class Meta:
        app_label="wiki_feedback"
        db_table = "wiki_feedback"
