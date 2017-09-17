# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-03 07:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('routes', '0003_add_validators'),
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('route_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='routes.Route')),
                ('raw_html', models.TextField(verbose_name='Raw HTML')),
            ],
            options={
                'abstract': False,
            },
            bases=('routes.route',),
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('base_objects', django.db.models.manager.Manager()),
            ],
        ),
    ]
