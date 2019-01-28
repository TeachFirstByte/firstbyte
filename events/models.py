from django.db import models
from django.urls import reverse
from django.utils.text import slugify

class Event(models.Model):
    title = models.CharField(max_length=200)
    event_image_path = models.CharField(max_length=256)
    start_datetime = models.DateTimeField()
    duration = models.DurationField()
    blurb = models.TextField()
    description = models.TextField()

    @property
    def slug(self):
        return slugify(self.title)

    @property
    def end_datetime(self):
        return self.start_datetime + self.duration

    def get_absolute_url(self):
        return reverse('detail-event', kwargs={
            'pk': self.id,
            'slug': self.slug
        })

    def __str__(self):
        return '(Event) ' + str(self.title)
