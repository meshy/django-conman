# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('routes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='route',
            name='url',
            field=models.TextField(db_index=True, unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='route',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='route',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='route',
            name='slug',
        ),
    ]
