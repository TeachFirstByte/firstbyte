from django.urls import path
from django.views.generic.list import ListView

from rest_framework import routers

from . import models
from . import views
from . import api

urlpatterns = [
    path('lesson-plans/new/', views.create_lesson_plan_view, name='create-lesson-plan'),
    path('lesson-plans/update/<int:pk>/', views.update_lesson_plan_view, name='update-lesson-plan'),
    path('lesson-plans/delete/<int:pk>/', views.DeleteLessonPlanView.as_view(), name='delete-lesson-plan'),

    path('lesson-plans/<int:pk>/', views.slug_redirect_view(models.LessonPlan)),
    path('lesson-plans/<int:pk>/<slug:slug>/', views.LessonPlanView.as_view(), name='detail-lesson-plan'),

    path('lesson-plans/', views.list_lessonplans, name='list-lesson-plan'),

    path('website-feedbacks/new', views.SubmitWebsiteFeedbackView.as_view(), name='submit-website-feedback'),
    path('website-feedbacks/thank-you/', views.website_feedback_done, name='website-feedback-done'),

    path('lesson-resources/', views.create_lesson_resource, name='create-lesson-resource'),
    path('lesson-resources/<int:pk>/', views.lesson_resource, name='detail-lesson-resource'),

    path('api/v1/lesson-plans/<int:pk>/', api.get_lessonplan),
]

router = routers.SimpleRouter()
router.register("api/v2/lesson-plans", api.LessonPlanViewSet)
urlpatterns.extend(router.urls)