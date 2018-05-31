# Generated by Django 2.0.5 on 2018-05-31 02:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school', models.CharField(max_length=200)),
                ('grade_level', models.CharField(choices=[('ES', 'Elementary School'), ('MS', 'Middle School'), ('HS', 'High School'), ('U', 'Post-secondary')], max_length=2)),
                ('proficiency_description', models.CharField(choices=[('newbie', 'Completely new to STEM (primarily the Technology part).'), ('nerd', 'Familiar with STEM and currently looking to bring it into the classroom.'), ('oldie', "Took classes in post-secondary education, but haven't touched it since."), ('veteran', 'Very familiar with STEM and its use in the classroom.')], max_length=7)),
                ('wants_email', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
