from django.urls import include, path

from . import views

urlpatterns = [
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    # login, logout, password_change, password_reset (+ done, confirm, complete)
    path('', include('django.contrib.auth.urls')),
]
