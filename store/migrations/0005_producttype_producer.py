# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-14 04:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_auto_20171013_1759'),
    ]

    operations = [
        migrations.AddField(
            model_name='producttype',
            name='producer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='store.Producer'),
        ),
    ]
