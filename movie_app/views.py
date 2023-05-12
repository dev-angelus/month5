from datetime import timedelta

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination

from .models import Director, Movie, Review
from .serializers import DirectorSerializer, MovieSerializer, ReviewSerializer, \
    RatingSerializer, DirectorValidateSerializer, MovieValidateSerializer, ReviewValidateSerializer


class DirectorListAPIView(ListCreateAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer
    pagination_class = PageNumberPagination


class DirectorDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer
    pagination_class = PageNumberPagination
    lookup_field = 'id'


class MovieListAPIView(ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    pagination_class = PageNumberPagination

    def post(self, request, *args, **kwargs):
        """ VALIDATE DATA """
        serializer = MovieValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data={'errors': serializer.errors},
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        title = serializer.validated_data.get('title')
        description = serializer.validated_data.get('description')
        duration_string = request.data.get('duration')
        duration_parts = duration_string.split(':')
        duration = timedelta(hours=int(duration_parts[0]), minutes=int(duration_parts[1]),
                             seconds=int(duration_parts[2]))
        director_id = request.data.get('director_id')
        genres = serializer.validated_data.get('genres')
        movie_obj = Movie.objects.create(title=title, description=description, duration=duration,
                                         director_id=director_id)
        movie_obj.genres.set(genres)
        movie_obj.save()
        return Response(data=MovieSerializer(movie_obj).data)


class MovieDetailListApiView(RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    pagination_class = PageNumberPagination
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        movie_obj = Movie.objects.get(id=id)
        serializer = MovieValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        movie_obj.title = serializer.validated_data.get('title')
        movie_obj.description = serializer.validated_data.get('description')
        duration_string = request.data.get('duration')
        duration_parts = duration_string.split(':')
        movie_obj.duration = timedelta(hours=int(duration_parts[0]), minutes=int(duration_parts[1]),
                                   seconds=int(duration_parts[2]))
        movie_obj.director_id = serializer.validated_data.get('director_id')
        movie_obj.genres.set(serializer.validated_data.get('genres'))
        movie_obj.save()
        return Response(data=MovieSerializer(movie_obj).data)


class MovieReviewsRatingView(ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = RatingSerializer
    pagination_class = PageNumberPagination


class ReviewListApiView(ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination


class ReviewDetailListApiView(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination
    lookup_field = 'id'



