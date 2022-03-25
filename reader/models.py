from django.db.models import JSONField, Model
from django.contrib.auth.models import User
from django.db import models

from django.utils import timezone

class Course(Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, default="Course")
    course_structure = JSONField()

    def __str__(self):
        return self.name

class Group(models.Model):
    id = models.CharField(primary_key=True, max_length=100, default="group")
    name = models.CharField(max_length=100, default="group")
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    students = models.ManyToManyField(User)

    def __str__(self):
        return self.name

class Resource(models.Model):
    id = models.CharField(primary_key=True,max_length=100, default="resource")
    name = models.CharField(max_length=100, default="book")
    type = models.CharField(max_length=100, default="book")#e.g. book, tutorial, paper
    format = models.CharField(max_length=5, default="pdf")
    file = models.CharField(max_length=100, default="book")

    def __str__(self):
        return self.name

class ReadingLog(models.Model):
    id = models.AutoField(primary_key=True)
    datetime = models.DateTimeField(default=timezone.now)
    session = models.CharField(max_length=100, default="test")
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    group = models.ForeignKey(Group, default=1, on_delete=models.CASCADE)
    section = models.CharField(max_length=100, default="test")
    resource = models.CharField(max_length=100, default="book")
    page = models.IntegerField(default=0)
    visible_text = JSONField(blank=True)
    action = models.CharField(max_length=50, default="unknown")# e.g. page-load,zoom,scroll
    zoom = models.DecimalField(max_digits=4,decimal_places=2,default=1.0)
    extra = JSONField(blank=True)

class Feedback(models.Model):
    datetime = models.DateTimeField(default=timezone.now)
    session = models.CharField(max_length=100, default="test")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, default=1, on_delete=models.CASCADE)
    section = models.CharField(max_length=100, default="test")
    resource = models.CharField(max_length=100, default="book")
    page = models.IntegerField(default=0)
    type = models.CharField(max_length=100, default="test") #Type of feedback: difficulty (diff) or relevance (rel)
    target_type = models.CharField(max_length=100, default="test") #Type of target: video, page, etc.
    target_id = models.CharField(max_length=100, default="test")
    value = models.CharField(max_length=100, default="-1")
    explanation = models.CharField(max_length=100, default="")

class Assignment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, default=1, on_delete=models.CASCADE)
    section = models.CharField(max_length=100, default="test")
    type = models.CharField(max_length=100, default="test")  # Type of assignment: e.g. concept map
    datetime_start = models.DateTimeField(default=timezone.now)
    datetime_end = models.DateTimeField(default=timezone.now)
