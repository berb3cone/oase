# Generated by Django 2.2.2 on 2019-06-23 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_auto_20190623_1313'),
    ]

    operations = [
        migrations.AddField(
            model_name='loan_client',
            name='receiving_income',
            field=models.CharField(choices=[('this bank', 'THIS BANK'), ('other bank', 'OTHER BANK')], default='other bank', max_length=10),
            preserve_default=False,
        ),
    ]
