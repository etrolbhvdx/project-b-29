# Generated by Django 3.2.18 on 2023-05-01 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0006_message_as_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='deniedtransfer',
            name='reason',
            field=models.CharField(default='None', max_length=200),
        ),
    ]
