from __future__ import unicode_literals
from django.db import models
from tinymce.models import HTMLField
from django.contrib.auth.models import User

class Post(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=60)
    description = models.TextField(blank=True, default='')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now=True)
    votes = models.IntegerField(default=0)
    is_question = models.BooleanField(default=True)
    """creator = models.ForeignKey(User, blank=True, null=True)"""

class Result(models.Model):
    votes = models.IntegerField(default=0)

class Survey(models.Model):
    total = models.IntegerField(default=0)

class SurveyOffer(models.Model):
    user = models.ForeignKey(User)
    survey_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=60)
    questions = models.TextField(blank=True, default='')
    #time = models.TimeField()


class InapproptiateWord(models.Model):
    word = models.CharField(max_length=60)

    def __unicode__(self):
        return self.word

class FeedbackFromOnePreson(models.Model):
    user = models.ForeignKey(User)
    survey_id = models.IntegerField()
    result_key = models.CharField(max_length=100)
    result_value = models.CharField(max_length=100)

class Dicty(models.Model):
    name = models.CharField(max_length=100)

class FeedbackStatistics(models.Model):

    question = models.CharField(max_length=70)
    avg_vote = models.FloatField()





# Create your models here.
