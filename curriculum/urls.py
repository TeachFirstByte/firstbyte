from django.urls import path
from django.views.generic.list import ListView
from . import models
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('lesson-plan/new/', views.CreateLessonPlanView.as_view(), name='create-lesson-plan'),
    path('lesson-plan/<int:pk>/', views.LessonPlanView.as_view(), name='detail-lesson-plan'),
    path('lesson-plan/all/', ListView.as_view(model=models.LessonPlan), name='list-lesson-plan'),
    path('lesson-plan/by-user/<int:pk>', views.LessonPlanUserList.as_view(), name='user-lesson-plans'),
    path('submit-website-feedback/', views.SubmitWebsiteFeedbackView.as_view(), name='submit-website-feedback'),
    path('website-feedback-done/', views.website_feedback_done, name='website-feedback-done'),
    path('lesson-resource/', views.create_lesson_resource, name='create-lesson-resource'),
    path('lesson-resource/<int:pk>/', views.lesson_resource, name='detail-lesson-resource')
]
