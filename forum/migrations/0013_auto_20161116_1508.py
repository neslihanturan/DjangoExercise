# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-16 15:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0012_remove_surveyoffer_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='surveyoffer',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
