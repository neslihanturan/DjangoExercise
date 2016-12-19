# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-05 19:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0017_auto_20161205_1301'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dicty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='feedbackfromonepreson',
            name='result_key',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='feedbackfromonepreson',
            name='result_value',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
