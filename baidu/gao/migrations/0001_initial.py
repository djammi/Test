# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Passport',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('is_delete', models.BooleanField(verbose_name='刪除時間', default=False)),
                ('create_time', models.DateTimeField(verbose_name='創建時間', auto_now_add=True)),
                ('update_time', models.DateTimeField(verbose_name='更新時間', auto_now=True)),
                ('username', models.CharField(verbose_name='用戶名稱', max_length=20)),
                ('password', models.CharField(verbose_name='用戶密碼', max_length=20)),
                ('email', models.EmailField(verbose_name='用戶郵箱', max_length=254)),
                ('is_active', models.BooleanField(verbose_name='激活狀體', default=False)),
            ],
            options={
                'db_table': 's_user_account',
            },
        ),
    ]
