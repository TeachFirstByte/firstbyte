# Generated by Django 2.1.5 on 2019-01-27 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='blurb',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]