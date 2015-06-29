# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('keyword_ideas', '0003_auto_20150627_1927'),
    ]

    operations = [
        migrations.AddField(
            model_name='keyword',
            name='mean_external_links',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='keyword',
            name='median_external_links',
            field=models.FloatField(null=True, blank=True),
        ),
    ]
