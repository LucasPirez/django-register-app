# Generated by Django 4.0.2 on 2022-04-04 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gymapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classname',
            name='duration',
            field=models.IntegerField(null=True),
        ),
    ]
