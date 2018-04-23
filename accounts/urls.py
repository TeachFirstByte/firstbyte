from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('me/', views.me, name='me'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/basic_form.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path(
        'password_change/',
        auth_views.PasswordChangeView.as_view(template_name='registration/basic_form.html'),
        name='password_change'),
    path(
        'password_change_done/',
        auth_views.PasswordChangeDoneView.as_view(),
        name='password_change_done'),
    path(
        'password_reset/',
        auth_views.PasswordResetView.as_view(template_name='registration/basic_form.html'),
        name='password_reset'),
    path(
        'password_reset_done/',
        auth_views.PasswordResetDoneView.as_view(),
        name='password_reset_done'),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name='registration/basic_form.html'),
        name='password_reset_confirm'),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete'),
]
