from django.db import models
from django.conf import settings
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


# Associate tags with LessonPlan
register(LessonPlan)

