"""firstbyte URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from landing.views import index, faq, privacy_policy, loaner_program, volunteer_redirect, media_release_form_redirect, inventory_form_redirect, student_feedback_form_redirect, teacher_pre_survey_redirect, teacher_check_in_1_redirect, teacher_check_in_2_redirect, teacher_post_survey, get_involved

urlpatterns = [

    path('user/', include('accounts.urls')),
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('frequently-asked-questions/', faq, name='faq'),
    path('privacy-policy/', privacy_policy, name='privacy-policy'),
    path('loaner-program/', loaner_program, name='loaner-program'),
    # Temporary swap these endpoints so that our flyer gets them to the
    # get involved page (which we agreed was more newbie-friendly).
    path('volunteer/', get_involved, name='get-involved'),
    path('get-involved/', volunteer_redirect, name='volunteer-redirect'),
    path('media-release-form/', media_release_form_redirect, name='media-release-form'),
    path('photo-release/', media_release_form_redirect),
    path('inventory/', inventory_form_redirect),
    path('student-feedback/', student_feedback_form_redirect),
    path('pre-survey/', teacher_pre_survey_redirect),
    path('checkin-1/', teacher_check_in_1_redirect),
    path('checkin-2/', teacher_check_in_2_redirect),
    path('post-survey/', teacher_post_survey),
    path('', include('curriculum.urls')),
]
