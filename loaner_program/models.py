from django.db import models


class Technology(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField()
    image_url_path = models.CharField(max_length=200)


class Kit(models.Model):
    technology_id = models.ForeignKey('Technology')
    num_boards = models.PositiveIntegerField()


class Reservation_Request(models.Model):
    user_id = models.ForeignKey('User')
    technology_id = models.ForeignKey('Technology')
    start_time = models.DateField()
    end_time = models.DateField()
    minimum_boards_required = models.PositiveIntegerField()
    status = models.CharField(max_length=200)


class Reservation(models.Model):
    user_id = models.ForeignKey('User')
    kit_id = models.ForeignKey('Kit')
    start_time = models.DateField()
    end_time = models.DateField()
    request_id = models.ForeignKey('Reservation_Request')
