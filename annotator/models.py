import uuid

from django.db import models
from django.contrib.auth.models import User
from reader import models as reader_models
from django_mysql.models import JSONField, Model

from django.utils import timezone


class Annotation(models.Model):
    """
    Follows the `Annotation format <http://docs.annotatorjs.org/en/v1.2.x/annotation-format.html>`_,
    of ``annotatorjs``.

    :param annotator_schema_version: schema version: default v1.0
    :param created: created datetime
    :param updated: updated datetime
    :param text: content of annotation
    :param quote: the annotated text
    :param uri: URI of annotated document
    :param user: user id of annotation owner
    :param consumer: consumer key of backend
    """
    #id = models.AutoField(primary_key=True)
    id = models.CharField(max_length=10, primary_key=True, default="0000000000")
    annotator_schema_version = models.CharField(max_length=8, default="v1.0")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    text = models.TextField()
    quote = models.TextField()
    uri = models.CharField(max_length=4096, blank=True)
    group = models.ForeignKey(reader_models.Group, default="default")
    user = models.ForeignKey(User)
    username = models.CharField(max_length=32, default="test", blank=True)
    consumer = models.CharField(max_length=64, blank=True)
    permissions = JSONField()

    class Meta:
        ordering = ("created",)


class Range(models.Model):
    """
    Follows the `Annotation format <http://docs.annotatorjs.org/en/v1.2.x/annotation-format.html>`_,
    of ``annotatorjs``.

    :param start: (relative) XPath to start element
    :param end: (relative) XPath to end element
    :param startOffset: character offset within start element
    :param endOffset: character offset within end element
    :param annotation: related ``Annotation``
    """
    start = models.CharField(max_length=128)
    end = models.CharField(max_length=128)
    startOffset = models.IntegerField()
    endOffset = models.IntegerField()
    annotation = models.ForeignKey(Annotation, related_name="ranges")


"""
class Annotation(EmbeddedDocument):
    annotator_schema_version = StringField(max_length=8, default="v1.0")
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)
    text = StringField()
    quote = StringField()

    uri = StringField(max_length=4096, blank=True)
    user = StringField(max_length=128, blank=True)
    consumer = StringField(max_length=64, blank=True)

    ranges = ListField(EmbeddedDocumentField('Range'), required=True)


class Range(Document):
    start = StringField(max_length=128)
    end = StringField(max_length=128)
    startOffset = IntField()
    endOffset = IntField()

"""
