# Generated by Django 5.0.6 on 2024-07-20 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SmartSeating', '0006_studentcompletedetails'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentcompletedetails',
            name='branch',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='studentcompletedetails',
            name='year',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
