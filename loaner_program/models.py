from django.db import models

class Technology(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField()
    image_url_path = models.CharField(max_length=200)

