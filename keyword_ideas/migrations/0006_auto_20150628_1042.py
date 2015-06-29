# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('keyword_ideas', '0005_auto_20150628_1002'),
    ]

    operations = [
        migrations.RenameField(
            model_name='keyword',
            old_name='text',
            new_name='phrase',
        ),
        migrations.RenameField(
            model_name='seedkeyword',
            old_name='text',
            new_name='phrase',
        ),
        migrations.AlterUniqueTogether(
            name='keyword',
            unique_together=set([('seed_keyword', 'phrase')]),
        ),
    ]
