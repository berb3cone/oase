# Generated by Django 2.2.2 on 2019-06-19 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20190617_1752'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loan_client',
            name='loan_history',
            field=models.CharField(choices=[('ok', 'OK'), ('not ok', 'NOT OK')], help_text='official loan record obtained from loan office', max_length=6),
        ),
        migrations.AlterField(
            model_name='loan_client',
            name='needed_loan',
            field=models.IntegerField(default=20000, help_text='the amount requested by the client, in RON'),
        ),
        migrations.AlterField(
            model_name='loan_client',
            name='return_period',
            field=models.IntegerField(default=2, help_text='the number of years to return the loan'),
        ),
        migrations.AlterField(
            model_name='loan_client',
            name='work_experience',
            field=models.IntegerField(default=0, help_text='official records of work experience (in years)'),
        ),
    ]