from django.urls import path
from users import views

urlpatterns = [
    path('authorization/', views.authorization_api_view),
    path('registration/', views.registration_api_view),
    path('confirm/', views.confirm_api_view)
]