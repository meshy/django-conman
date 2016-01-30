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
                ('slug', models.SlugField(help_text='\n        Used to create the location of the Route. The Root Route needs\n        "slug" to be blank; all other Routes need a value unique to the parent.\n        It can only contain letters, numbers, underscores, or hyphens.\n    ', default='', max_length=255)),
                ('url', models.TextField(unique=True, editable=False, db_index=True)),
                ('parent', models.ForeignKey(blank=True, null=True, related_name='children', to='routes.Route')),
                ('polymorphic_ctype', models.ForeignKey(null=True, related_name='polymorphic_routes.route_set+', editable=False, to='contenttypes.ContentType')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='route',
            unique_together=set([('parent', 'slug')]),
        ),
    ]
