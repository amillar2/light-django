# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-20 02:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('esp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='espID',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='device',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='pwm',
            name='name',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='pwm',
            name='room',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='pwm',
            name='topic',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='switch',
            name='name',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='switch',
            name='room',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='switch',
            name='topic',
            field=models.CharField(max_length=50),
        ),
    ]
