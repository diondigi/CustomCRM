# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-02 08:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0003_auto_20170902_0226'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='roles',
            field=models.ManyToManyField(blank=True, to='crm.Role', verbose_name='角色'),
        ),
    ]
