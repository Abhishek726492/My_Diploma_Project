# Generated by Django 5.0.6 on 2024-07-20 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SmartSeating', '0004_studentdetails'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentdetails',
            name='year',
            field=models.CharField(max_length=10),
        ),
    ]