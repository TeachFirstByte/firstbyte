from django.urls import path
from . import views

urlpatterns = [
    path('loaner-program/', views.show_loaner_program, name='loaner-program')
]