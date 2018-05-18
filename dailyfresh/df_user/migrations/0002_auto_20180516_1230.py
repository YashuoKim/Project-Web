# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('df_user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='uaddress',
            field=models.CharField(default=b'', max_length=100),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='uphone',
            field=models.CharField(default=b'', max_length=11),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='upostcode',
            field=models.CharField(default=b'', max_length=6),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='ureceiver',
            field=models.CharField(default=b'', max_length=20),
        ),
    ]
