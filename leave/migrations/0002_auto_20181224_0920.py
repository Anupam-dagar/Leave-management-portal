# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-12-24 09:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leave', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='available_leaves',
            field=models.IntegerField(default=25),
        ),
    ]