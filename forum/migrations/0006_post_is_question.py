# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-31 09:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0005_post_votes'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='is_question',
            field=models.BooleanField(default=True),
        ),
    ]
