from django.urls import path
from . import views

urlpatterns = [
    path('lesson-plan/new/', views.CreateLessonPlanView.as_view(), name='create-lesson-plan'),
    path('lesson-plan/<int:pk>/', views.LessonPlanView.as_view(), name='detail-lesson-plan'),
    path('lesson-plan/all/', views.LessonPlanList.as_view(), name='list-lesson-plan'),
]
