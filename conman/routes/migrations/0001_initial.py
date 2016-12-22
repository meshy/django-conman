# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('slug', models.SlugField(max_length=255, default='', help_text='The url fragment at this point in the Route hierarchy.')),
                ('url', models.TextField(unique=True, editable=False, db_index=True)),
                ('parent', models.ForeignKey(blank=True, null=True, related_name='children', to='routes.Route', on_delete=models.CASCADE)),
                ('polymorphic_ctype', models.ForeignKey(null=True, related_name='polymorphic_routes.route_set+', editable=False, to='contenttypes.ContentType', on_delete=models.CASCADE)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='route',
            unique_together=set([('parent', 'slug')]),
        ),
    ]
