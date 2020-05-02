from django.urls import path
from landing import views

urlpatterns = [
    path('loaner-program/', views.loaner_program, name='loaner-program')
]
