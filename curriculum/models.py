from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import reverse
from tagging.registry import register


def user_upload_directory(instance, filename):
    """Return the upload directory for a given File (should have an owner)."""
    return 'user_{0}/{1}'.format(instance.owner.id, filename)


class LessonResource(models.Model):
    STUDENT_HANDOUT = 0
    TEACHER_REFERENCE = 1
    SLIDES = 2
    CODE = 3
    SCHEMATIC = 4

    FILE_TYPES = (
        (STUDENT_HANDOUT, "Student handout"),
        (TEACHER_REFERENCE, "Teacher reference"),
        (SLIDES, "Slides"),
        (CODE, "Code"),
        (SCHEMATIC, "Schematic"),
    )

    # The original filename - or whatever is displayed.
    name = models.CharField(max_length=60)

    # The type of document
    type = models.SmallIntegerField(choices=FILE_TYPES)

    # The uploader of the file, should only be null if a user is deleted.
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    # The actual reference to the file on the filesystem.
    file = models.FileField(upload_to=user_upload_directory)


class LessonPlan(models.Model):
    ELEMENTARY_SCHOOL_LEVEL = 'ES'
    MIDDLE_SCHOOL_LEVEL = 'MS'
    HIGH_SCHOOL_LEVEL = 'HS'

    GradeLevel = (
        (ELEMENTARY_SCHOOL_LEVEL, "Elementary School"),
        (MIDDLE_SCHOOL_LEVEL, "Middle School"),
        (HIGH_SCHOOL_LEVEL, "High School"),
    )

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    title = models.CharField(max_length=120, unique=True)
    grade_level = models.CharField(max_length=2, choices=GradeLevel)

    prep_time = models.DurationField()
    class_time = models.DurationField()

    # Summary and materials listing
    summary = models.CharField(max_length=2000)
    materials = models.CharField(max_length=2000)

    # uploaded files!
    resources = models.ManyToManyField(LessonResource, blank=True)

    # enable feedback?
    feedback_enabled = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse('detail-lesson-plan', kwargs={'pk': self.id})


# Associate tags with LessonPlan
register(LessonPlan)


class FiveStarRatingField(models.SmallIntegerField):
    ratings = (
        (1, "One star"),
        (2, "Two stars"),
        (3, "Three stars"),
        (4, "Four stars"),
        (5, "Five stars"),
    )

    def __init__(self, *args, **kwargs):
        kwargs['choices'] = kwargs.get('choices', self.ratings)
        super().__init__(*args, **kwargs)


class LessonFeedback(models.Model):
    lesson = models.ForeignKey(LessonPlan, null=True, on_delete=models.SET_NULL)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    # 1 star = complete failure; 5 stars = complete success
    overall_rating = FiveStarRatingField()

    # 2500 characters is appox. 2-3 meaty paragraphs.
    strengths = models.TextField(max_length=2500)
    weaknesses = models.TextField(max_length=2500)


class WebsiteFeedback(models.Model):
    # 1 star = complete failure; 5 stars = complete success
    overall_rating = FiveStarRatingField()

    # 2500 characters is appox. 2-3 meaty paragraphs.
    strengths = models.TextField(max_length=2500)
    weaknesses = models.TextField(max_length=2500)
