from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.RegistrationAPIView.as_view(), name='register'),
    path('login/', views.LoginAPIView.as_view(), name='login'),
]
