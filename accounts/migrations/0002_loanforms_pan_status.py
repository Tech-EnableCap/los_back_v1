# Generated by Django 3.2.5 on 2021-08-23 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='loanforms',
            name='pan_status',
            field=models.CharField(default='not_chked', max_length=255),
        ),
    ]
