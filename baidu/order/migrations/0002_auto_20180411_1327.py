# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderinfo',
            name='pay_method',
            field=models.SmallIntegerField(verbose_name='支付方式', default=1, choices=[(2, '待发货'), (5, '已完成'), (1, '待支付'), (4, '待评价'), (3, '待收货')]),
        ),
        migrations.AlterField(
            model_name='orderinfo',
            name='status',
            field=models.SmallIntegerField(verbose_name='订单状态', default=1, choices=[(2, '待发货'), (5, '已完成'), (1, '待支付'), (4, '待评价'), (3, '待收货')]),
        ),
    ]
