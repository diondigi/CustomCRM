# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-04 13:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0005_customer_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='合同名称')),
                ('content', models.TextField(blank=True, null=True, verbose_name='合同内容')),
            ],
        ),
        migrations.AddField(
            model_name='customer',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='常用邮箱'),
        ),
        migrations.AddField(
            model_name='customer',
            name='id_num',
            field=models.CharField(blank=True, max_length=18, null=True, verbose_name='身份证'),
        ),
        migrations.AlterField(
            model_name='enrollment',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.Customer', verbose_name='客户'),
        ),
        migrations.AddField(
            model_name='enrollment',
            name='contract',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='crm.Contract', verbose_name='合同'),
        ),
    ]
