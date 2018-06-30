from django.db import models
from django.contrib.auth.models import User

ELEMENTARY_SCHOOL_LEVEL = 'ES'
MIDDLE_SCHOOL_LEVEL = 'MS'
HIGH_SCHOOL_LEVEL = 'HS'
POST_SECONDARY_LEVEL = 'U'

GRADE_LEVEL_MAX_LENGTH = 2
GradeLevels = (
    (ELEMENTARY_SCHOOL_LEVEL, "Elementary School"),
    (MIDDLE_SCHOOL_LEVEL, "Middle School"),
    (HIGH_SCHOOL_LEVEL, "High School"),
    (POST_SECONDARY_LEVEL, "Post-secondary")
)

NEWBIE_PROFICIENCY = 'newbie'
NERD_PROFICIENCY = 'nerd'
OLDIE_PROFICIENCY = 'oldie'
VETERAN_PROFICIENCY = 'veteran'

TEACHER_PROFICIENCY_MAX_LENGTH = 7
TeacherProficiencies = (
    (NEWBIE_PROFICIENCY, 'Completely new to STEM (primarily the Technology part).'),
    (NERD_PROFICIENCY, "Familiar with STEM and currently looking to bring it into the classroom."),
    (OLDIE_PROFICIENCY, "Took classes in post-secondary education, but haven't touched it since."),
    (VETERAN_PROFICIENCY, "Very familiar with STEM and its use in the classroom.")
)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school = models.CharField(blank=True, max_length=200)
    grade_level = models.CharField(blank=True, max_length=GRADE_LEVEL_MAX_LENGTH, choices=GradeLevels)
    proficiency_description = models.CharField(blank=True, max_length=TEACHER_PROFICIENCY_MAX_LENGTH, choices=TeacherProficiencies)
    wants_email = models.BooleanField(default=False)
