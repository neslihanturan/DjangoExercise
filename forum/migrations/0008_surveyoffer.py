# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-31 19:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0007_survey'),
    ]

    operations = [
        migrations.CreateModel(
            name='SurveyOffer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=60)),
                ('questions', models.TextField(blank=True, default='')),
            ],
        ),
    ]
