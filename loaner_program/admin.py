from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Technology)
admin.site.register(models.Kit)
admin.site.register(models.Reservation)
admin.site.register(models.ReservationRequest)
