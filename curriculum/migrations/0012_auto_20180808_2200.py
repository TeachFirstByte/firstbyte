# Generated by Django 2.0.7 on 2018-08-08 22:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('curriculum', '0011_auto_20180707_0436'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lessonfeedback',
            old_name='strengths',
            new_name='comments',
        ),
        migrations.RemoveField(
            model_name='lessonfeedback',
            name='weaknesses',
        ),
    ]
