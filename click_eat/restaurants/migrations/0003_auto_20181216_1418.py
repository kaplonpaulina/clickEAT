# Generated by Django 2.1.2 on 2018-12-16 14:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0002_auto_20181216_1406'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='restaurant',
            name='update_date',
        ),
        migrations.AddField(
            model_name='restaurant',
            name='author',
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
