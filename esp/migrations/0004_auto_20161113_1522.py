# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-13 21:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('esp', '0003_auto_20161101_2006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='switch',
            name='pwm',
            field=models.ManyToManyField(blank=True, to='esp.PWM'),
        ),
    ]