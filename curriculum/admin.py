from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.LessonResource)
admin.site.register(models.LessonPlan)
admin.site.register(models.LessonFeedback)
admin.site.register(models.WebsiteFeedback)
