# Generated by Django 2.0.2 on 2018-03-18 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0003_auto_20180318_1858'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='person_id',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='age',
            field=models.PositiveIntegerField(null=True),
        ),
    ]