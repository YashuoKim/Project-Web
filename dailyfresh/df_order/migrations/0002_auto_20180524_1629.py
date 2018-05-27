# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('df_order', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderinfo',
            name='opay',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='orderinfo',
            name='oaddress',
            field=models.CharField(default=b'', max_length=150),
        ),
    ]
