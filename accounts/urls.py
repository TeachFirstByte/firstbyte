from django.urls import path, include
from . import views

urlpatterns = [
    path('me/', views.me, name='me'),
    path('<int:pk>/', views.user_detail, name='user-detail'),
    path('', include('allauth.urls')),
]
