# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-21 16:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('routes', '0003_add_validators'),
    ]

    operations = [
        migrations.CreateModel(
            name='RouteSubclass',
            fields=[
                ('route_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='routes.Route')),
            ],
            options={
                'abstract': False,
            },
            bases=('routes.route',),
        ),
        migrations.CreateModel(
            name='TemplateRoute',
            fields=[
                ('route_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='routes.Route')),
                ('content', models.TextField()),
            ],
            options={
                'abstract': False,
            },
            bases=('routes.route',),
        ),
        migrations.CreateModel(
            name='URLConfRoute',
            fields=[
                ('route_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='routes.Route')),
            ],
            options={
                'abstract': False,
            },
            bases=('routes.route',),
        ),
        migrations.CreateModel(
            name='NestedRouteSubclass',
            fields=[
                ('routesubclass_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='tests.RouteSubclass')),
            ],
            options={
                'abstract': False,
            },
            bases=('tests.routesubclass',),
        ),
    ]
