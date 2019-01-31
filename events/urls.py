from django.urls import path
from . import views
from . import models
from firstbyte.views import slug_redirect_view

urlpatterns = [
    path('events/', views.event_list, name='list-event'),
    path('events/<int:pk>/', slug_redirect_view(models.Event)),
    path('events/<int:pk>/<slug:slug>/', views.event_detail, name='detail-event'),
]