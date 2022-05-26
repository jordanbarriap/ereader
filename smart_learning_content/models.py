from django.db.models import JSONField, Model
from django.db import models
from django.contrib.auth.models import User

from django.utils import timezone

# Create your models here.

class SmartContent(models.Model):
    content_id = models.AutoField(primary_key=True)
    content_name = models.CharField(max_length=100, default="activity")
    content_type = models.CharField(max_length=100, default="parsons")
    display_name = models.CharField(max_length=50, default="")
    desc = models.CharField(max_length=500,default="")
    url = models.CharField(max_length=2083, default="url", unique=True)
    domain = models.CharField(max_length=10,default="py")
    provider_id = models.CharField(max_length=100, default="parsons",unique=True)
    comment = models.CharField(max_length=100,default="")
    visible = models.BooleanField()
    creation_date = models.DateTimeField(default=timezone.now)
    creator_id = models.CharField(max_length=50, default="admin")
    privacy = models.CharField(max_length=50,default="public")
    author_name = models.CharField(max_length=50, default="")

    def __str__(self):
        return self.content_name

    class Meta:
        app_label="smart_learning_content"
        db_table = "smart_learning_content"