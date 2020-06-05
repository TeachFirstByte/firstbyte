from django.db import models
from django.contrib.auth.models import User

class Technology(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField()
    image_url_path = models.CharField(max_length=200)


class Kit(models.Model):
    technology = models.ForeignKey('Technology', on_delete=models.CASCADE)
    num_boards = models.PositiveIntegerField()


class ReservationRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    technology_id = models.ForeignKey('Technology', on_delete=models.DO_NOTHING)
    start_time = models.DateField()
    end_time = models.DateField()
    minimum_boards_required = models.PositiveIntegerField()
    status = models.CharField(max_length=200)


class Reservation(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    kit_id = models.ForeignKey('Kit', on_delete=models.DO_NOTHING)
    start_time = models.DateField()
    end_time = models.DateField()
    request = models.ForeignKey('ReservationRequest', on_delete=models.DO_NOTHING)
