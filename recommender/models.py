from django_mysql.models import JSONField, Model
from django.db import models
from django.contrib.auth.models import User

from reader import models as reader_models

from django.utils import timezone

# Create your models here.


class Resource(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=100, default="video")
    title = models.CharField(max_length=100, default="title")
    url = models.CharField(max_length=200, default="url", unique=True)
    length = models.IntegerField(default=0)
    datetime_added = models.DateTimeField(default=timezone.now)
    info_json = JSONField(blank=True)

    def __str__(self):
        return self.title


class Similarity(models.Model):
    resource_id = models.ForeignKey(Resource)
    id_textual_resource = models.CharField(max_length=100, default="page")
    type = models.CharField(max_length=100, default="cosine")
    value = models.FloatField(default=.0)


class Rating(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User)
    group = models.ForeignKey(reader_models.Group, default=1)
    resource = models.ForeignKey(Resource)
    section = models.CharField(max_length=100, default="test")
    page = models.IntegerField(default=0)
    type = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    explanation = models.CharField(max_length=1000, default="")
    session = models.CharField(max_length=100, default="test")
    datetime = models.DateTimeField(default=timezone.now)
    extra = JSONField(blank=True)



