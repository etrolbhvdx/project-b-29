# Generated by Django 4.1.6 on 2023-03-20 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0003_message_school_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='equivalency_name',
            field=models.CharField(default='None', max_length=200),
        ),
    ]