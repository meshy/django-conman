# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import conman.routes.validators


class Migration(migrations.Migration):

    dependencies = [
        ('routes', '0002_remove_slug_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='route',
            name='url',
            field=models.TextField(db_index=True, help_text='The operative URL for this Route.', validators=[conman.routes.validators.validate_end_in_slash, conman.routes.validators.validate_start_in_slash, conman.routes.validators.validate_no_dotty_subpaths, conman.routes.validators.validate_no_double_slashes, conman.routes.validators.validate_no_hash_symbol, conman.routes.validators.validate_no_questionmark], unique=True, verbose_name='URL'),
        ),
    ]
