# Generated by Django 2.2.2 on 2019-06-17 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20190617_1638'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='loan_client',
            name='tax_rate',
        ),
        migrations.AddField(
            model_name='loan_client',
            name='tax_percent',
            field=models.IntegerField(default=45),
        ),
    ]