# Generated by Django 2.2.2 on 2019-06-19 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_auto_20190620_0051'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='loan_client',
            name='cname',
        ),
        migrations.AddField(
            model_name='loan_client',
            name='first_name',
            field=models.CharField(default='x', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='loan_client',
            name='last_name',
            field=models.CharField(default='Alexandru', max_length=20),
            preserve_default=False,
        ),
    ]
