# Generated by Django 4.0.4 on 2023-04-17 01:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ApprovedTransfer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_name', models.CharField(max_length=200)),
                ('school_name', models.CharField(default='uva', max_length=200)),
                ('equivalency_name', models.CharField(default='None', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message_text', models.CharField(max_length=200)),
                ('school_name', models.CharField(default='uva', max_length=200)),
                ('equivalency_name', models.CharField(default='None', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Offering',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=200)),
                ('day', models.CharField(max_length=200)),
                ('enrollment', models.CharField(max_length=200)),
                ('if_full', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Transfer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transferClass', models.CharField(max_length=200)),
                ('title', models.CharField(max_length=200)),
                ('transferCredits', models.CharField(max_length=200)),
                ('UVAClass', models.CharField(max_length=200)),
                ('UVACredits', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=200)),
                ('is_admin', models.BooleanField(default=False)),
            ],
        ),
    ]
