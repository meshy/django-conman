# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-05 21:04
from __future__ import unicode_literals

import conman.routes.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('routes', '0003_add_validators'),
    ]

    operations = [
        migrations.AlterField(
            model_name='route',
            name='url',
            field=conman.routes.models.URLPathField(db_index=True, help_text='The operative URL for this Route.', unique=True, verbose_name='URL'),
        ),
    ]