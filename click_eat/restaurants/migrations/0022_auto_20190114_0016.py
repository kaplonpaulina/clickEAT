# Generated by Django 2.1.2 on 2019-01-14 00:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0021_auto_20190114_0014'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='body',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
