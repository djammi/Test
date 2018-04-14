# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_auto_20180411_1327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderinfo',
            name='pay_method',
            field=models.SmallIntegerField(verbose_name='支付方式', default=1, choices=[(1, '货到付款'), (2, '微信支付'), (3, '支付宝'), (4, '银联支付')]),
        ),
        migrations.AlterField(
            model_name='orderinfo',
            name='status',
            field=models.SmallIntegerField(verbose_name='订单状态', default=1, choices=[(1, '待支付'), (4, '待评价'), (2, '待发货'), (3, '待收货'), (5, '已完成')]),
        ),
    ]
