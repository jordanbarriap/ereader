from django.db.models import JSONField, Model
from django.contrib.auth.models import User
from reader import models as reader_models
from django.db import models

from django.utils import timezone


# Create your models here.
class ConceptMap(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(reader_models.Group, default=1, on_delete=models.CASCADE)
    session = models.CharField(max_length=100, default="test")
    section = models.CharField(max_length=100)
    structure = JSONField(blank=False)
    datetime = models.DateTimeField(default=timezone.now)
    context = JSONField(blank=True) # data about the context where the concept map was created

class ConceptMappingLog(models.Model):
    id = models.AutoField(primary_key=True)
    datetime = models.DateTimeField(default=timezone.now)
    session = models.CharField(max_length=100, default="test")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(reader_models.Group, default=1, on_delete=models.CASCADE)
    section = models.CharField(max_length=100, default="test")
    action = JSONField(blank=True)# e.g. add, delete, rename
    context = JSONField(blank=True)  # data about the context where the action was performed
    zoom = models.DecimalField(max_digits=4,decimal_places=2,default=1.0)
