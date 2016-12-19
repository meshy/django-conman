# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('routes', '0003_add_validators'),
        ('redirects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='URLRedirect',
            fields=[
                ('route_ptr', models.OneToOneField(to='routes.Route', auto_created=True, primary_key=True, serialize=False, parent_link=True)),
                ('target', models.URLField(max_length=2000)),
                ('permanent', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
            bases=('routes.route',),
        ),
    ]
