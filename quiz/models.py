from django.db import models
from django.contrib.auth.models import User
from django.db.models import JSONField, Model

from reader import models as reader_models

from django.utils import timezone
# Create your models here.


class Question(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=100, default="test")
    statement = models.CharField(max_length=1000, default="test")

    def __unicode__(self):
        return self.statement


class Choice(models.Model):
    id = models.AutoField(primary_key=True)
    statement = models.CharField(max_length=500, default="test")
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.statement


class Question_Correct_Answer(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)


"""class MCQuestion(models.Model):
    id = models.AutoField(primary_key=True)
    statement = models.CharField(max_length=500, default="test")
    answers = models.ManyToManyField(Answer)


class TextualQuestion(models.Model):
    id = models.AutoField(primary_key=True)
    statement = models.CharField(max_length=500, default="test")"""


class Quiz(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, default="book")
    course_section = models.CharField(max_length=100, default="0")
    questions = models.ManyToManyField(Question)

    def __unicode__(self):
        return self.name


class AnswerLog(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(reader_models.Group, default=1, on_delete=models.CASCADE)
    session = models.CharField(max_length=100, default="test")
    datetime = models.DateTimeField(default=timezone.now())
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = JSONField()
    correct = models.BooleanField(default=False)
    submitted = models.BooleanField(default=False)
    marked = models.BooleanField(default=True)


"""class TextualAnswerLog(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User)
    session = models.CharField(max_length=100, default="test")
    datetime = models.DateTimeField(default=timezone.now())
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.ForeignKey(MCQuestion, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)"""


class KC(models.Model):
    id = models.AutoField(primary_key=True)
    name= models.CharField(max_length=100, default="kc")


class KC_Section(models.Model):
    kc = models.ForeignKey(KC, on_delete=models.CASCADE)
    section = models.CharField(max_length=100, default="section")
    random = models.BooleanField(default=False)


class KCLevel(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    kc = models.ForeignKey(KC, on_delete=models.CASCADE)
    datetime = models.DateTimeField(default=timezone.now())
    level = models.IntegerField()

