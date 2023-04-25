# Generated by Django 3.2.17 on 2023-04-24 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0004_deniedtransfer'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeniedTransfer_AS',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_name', models.CharField(max_length=200)),
                ('school_name', models.CharField(default='uva', max_length=200)),
                ('equivalency_name', models.CharField(default='None', max_length=200)),
                ('user', models.CharField(default='None', max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='approvedtransfer_as',
            name='user',
            field=models.CharField(default='None', max_length=200),
        ),
    ]