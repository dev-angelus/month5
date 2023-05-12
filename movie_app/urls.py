from django.urls import path
from movie_app import views

urlpatterns = [
    path('directors/', views.DirectorListAPIView.as_view()),
    path('directors/<int:id>/', views.DirectorDetailAPIView.as_view()),
    path('movies/', views.MovieListAPIView.as_view()),
    path('movies/<int:id>/', views.MovieDetailListApiView.as_view()),
    path('movies/reviews/', views.MovieReviewsRatingView.as_view()),
    path('reviews/', views.ReviewListApiView.as_view()),
    path('reviews/<int:id>/', views.ReviewDetailListApiView.as_view()),
]
