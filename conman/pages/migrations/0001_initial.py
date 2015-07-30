# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sirtrevor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('routes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('route_ptr', models.OneToOneField(serialize=False, auto_created=True, parent_link=True, primary_key=True, to='routes.Route')),
                ('content', sirtrevor.fields.SirTrevorField(default='')),
            ],
            options={
                'ordering': ('tree_id', 'lft'),
                'abstract': False,
            },
            bases=('routes.route',),
        ),
    ]
