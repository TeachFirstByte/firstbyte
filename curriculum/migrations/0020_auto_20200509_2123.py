# Generated by Django 3.0.5 on 2020-05-09 21:23

from django.db import migrations
from sortedm2m.operations import AlterSortedManyToManyField
from sortedm2m import fields


class Migration(migrations.Migration):

    dependencies = [
        ('curriculum', '0019_auto_20200426_1822'),
    ]

    operations = [
        AlterSortedManyToManyField(
            model_name='lessonplan',
            name='materials',
            field=fields.SortedManyToManyField(blank=True, help_text=None, to='curriculum.Material'),
        ),
    ]