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
            name='slug',
            field=models.SlugField(max_length=255, help_text='The url fragment at this point in the Route hierarchy.', default=''),
        ),
    ]
