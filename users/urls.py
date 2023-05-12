from django.urls import path
from users import views

urlpatterns = [
    path('authorization/', views.AuthorizationAPIView.as_view()),
    path('registration/', views.RegistrationAPIView.as_view()),
    path('confirm/', views.ConfirmAPIView.as_view())
]