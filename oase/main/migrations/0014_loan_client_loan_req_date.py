# Generated by Django 2.2.2 on 2019-06-23 09:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_auto_20190620_0056'),
    ]

    operations = [
        migrations.AddField(
            model_name='loan_client',
            name='loan_req_date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
