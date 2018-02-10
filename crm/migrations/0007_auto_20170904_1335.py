# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-04 13:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0006_auto_20170904_1313'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contract',
            options={'verbose_name_plural': '合同表_Contract'},
        ),
        migrations.RemoveField(
            model_name='enrollment',
            name='contract',
        ),
        migrations.AddField(
            model_name='classlist',
            name='contract',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='crm.Contract', verbose_name='合同'),
        ),
    ]
