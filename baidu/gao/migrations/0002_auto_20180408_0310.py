# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gao', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passport',
            name='create_time',
            field=models.DateTimeField(verbose_name='创建时间', auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='passport',
            name='email',
            field=models.EmailField(verbose_name='用户邮箱', max_length=254),
        ),
        migrations.AlterField(
            model_name='passport',
            name='is_active',
            field=models.BooleanField(verbose_name='激活状态', default=False),
        ),
        migrations.AlterField(
            model_name='passport',
            name='is_delete',
            field=models.BooleanField(verbose_name='删除标记', default=False),
        ),
        migrations.AlterField(
            model_name='passport',
            name='password',
            field=models.CharField(verbose_name='用户密码', max_length=40),
        ),
        migrations.AlterField(
            model_name='passport',
            name='update_time',
            field=models.DateTimeField(verbose_name='更新时间', auto_now=True),
        ),
        migrations.AlterField(
            model_name='passport',
            name='username',
            field=models.CharField(verbose_name='用户名称', max_length=20),
        ),
    ]
