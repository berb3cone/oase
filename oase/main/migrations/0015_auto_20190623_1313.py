# Generated by Django 2.2.2 on 2019-06-23 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_loan_client_loan_req_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loan_client',
            name='loan_req_date',
            field=models.DateField(auto_now=True),
        ),
    ]
