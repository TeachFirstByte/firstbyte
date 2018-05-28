from django.urls import path, include
from . import views

urlpatterns = [
    path('me/', views.me, name='me'),
    path('', include('allauth.urls')),

]
