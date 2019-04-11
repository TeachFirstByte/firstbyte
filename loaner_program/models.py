from django.db import models


class Technology(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField()
    image_url_path = models.CharField(max_length=200)


class Kit(models.Model):
    technology = models.ForeignKey('Technology')
    num_boards = models.PositiveIntegerField()


class ReservationRequest(models.Model):
    user = models.ForeignKey('User')
    technology = models.ForeignKey('Technology')
    start_time = models.DateField()
    end_time = models.DateField()
    minimum_boards_required = models.PositiveIntegerField()
    status = models.CharField(max_length=200)


class Reservation(models.Model):
    user = models.ForeignKey('User')
    kit = models.ForeignKey('Kit')
    start_time = models.DateField()
    end_time = models.DateField()
    request = models.ForeignKey('ReservationRequest')
