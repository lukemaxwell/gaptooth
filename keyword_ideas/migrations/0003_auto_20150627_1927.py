# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('keyword_ideas', '0002_auto_20150627_1922'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='keyword',
            unique_together=set([('seed_keyword', 'text')]),
        ),
    ]
