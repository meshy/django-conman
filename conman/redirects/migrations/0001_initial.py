# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('routes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RouteRedirect',
            fields=[
                ('route_ptr', models.OneToOneField(serialize=False, auto_created=True, to='routes.Route', parent_link=True, primary_key=True)),
                ('permanent', models.BooleanField(default=False)),
                ('target', models.ForeignKey(to='routes.Route', related_name='+')),
            ],
            options={
                'abstract': False,
            },
            bases=('routes.route',),
        ),
    ]
