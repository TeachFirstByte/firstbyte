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

from landing.views import index, faq, privacy_policy, loaner_program, volunteer_redirect, get_involved

urlpatterns = [

    path('user/', include('accounts.urls')),
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('frequently-asked-questions/', faq, name='faq'),
    path('privacy-policy/', privacy_policy, name='privacy-policy'),
    path('loaner-program/', loaner_program, name='loaner-program'),
    path('get-involved/', get_involved, name='get-involved'),
    path('volunteer/', volunteer_redirect, name='volunteer-redirect'),
    path('', include('curriculum.urls')),
]
