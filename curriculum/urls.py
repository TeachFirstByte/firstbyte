from django.urls import path
from django.views.generic.list import ListView
from . import models
from . import views

urlpatterns = [
    path('lesson-plan/new/', views.CreateLessonPlanView.as_view(), name='create-lesson-plan'),
    path('lesson-plan/<int:pk>/', views.LessonPlanView.as_view(), name='detail-lesson-plan'),
    path('lesson-plan/all/', ListView.as_view(model=models.LessonPlan), name='list-lesson-plan'),
]
