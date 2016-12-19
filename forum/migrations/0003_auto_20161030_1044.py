# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-30 10:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0002_entry'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Forum',
            new_name='Post',
        ),
        migrations.AlterField(
            model_name='entry',
            name='description',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='entry',
            name='title',
            field=models.CharField(max_length=250, verbose_name='Ask your question'),
        ),
    ]
