# Generated by Django 2.1.2 on 2018-12-16 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0003_auto_20181216_1418'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
    ]
