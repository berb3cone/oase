# Generated by Django 2.2.2 on 2019-06-19 21:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_loan_client_cname'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='loan_client',
            name='cname',
        ),
    ]
