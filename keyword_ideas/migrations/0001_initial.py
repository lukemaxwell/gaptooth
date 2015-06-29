# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=100)),
                ('search_volume', models.IntegerField()),
                ('average_cpc', models.DecimalField(max_digits=5, decimal_places=2)),
                ('competition', models.FloatField()),
                ('mean_page_authority', models.FloatField(null=True, blank=True)),
                ('mean_domain_authority', models.FloatField(null=True, blank=True)),
                ('median_page_authority', models.FloatField(null=True, blank=True)),
                ('median_domain_authority', models.FloatField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='SeedKeyword',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='keyword',
            name='seed_keyword',
            field=models.ForeignKey(to='keyword_ideas.SeedKeyword'),
        ),
    ]
