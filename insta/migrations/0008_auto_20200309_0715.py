# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2020-03-09 07:15
from __future__ import unicode_literals

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('insta', '0007_auto_20200308_1631'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=cloudinary.models.CloudinaryField(max_length=255, verbose_name='images'),
        ),
    ]