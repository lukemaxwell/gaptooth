# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('keyword_ideas', '0004_auto_20150628_0950'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keyword',
            name='mean_domain_authority',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='keyword',
            name='mean_page_authority',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='keyword',
            name='median_domain_authority',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='keyword',
            name='median_page_authority',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
