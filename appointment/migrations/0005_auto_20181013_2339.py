# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-10-13 21:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0004_auto_20181013_2239'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bookappointment',
            old_name='is_patient',
            new_name='is_doctor',
        ),
    ]