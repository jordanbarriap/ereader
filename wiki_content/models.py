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