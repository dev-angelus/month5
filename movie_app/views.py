from datetime import timedelta

from rest_framework import status
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import Director, Movie, Review
from .serializers import DirectorSerializer, MovieSerializer, ReviewSerializer, \
    RatingSerializer, DirectorValidateSerializer, MovieValidateSerializer, ReviewValidateSerializer


class DirectorListAPIView(ListCreateAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer
    pagination_class = PageNumberPagination

    def post(self, request, *args, **kwargs):
        serializer = DirectorValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data={'errors': serializer.errors},
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        name = serializer.validated_data.get('name')
        director_obj = Director.objects.create(name=name)
        return Response(data=DirectorSerializer(director_obj).data)


class DirectorDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer
    pagination_class = PageNumberPagination
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        director_obj = Director.objects.get(id=id)
        serializer = DirectorValidateSerializer(data=request.data)
        director_obj.name = serializer.validated_data.get('name')
        return Response(data=DirectorSerializer(director_obj).data)


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

    def post(self, request, *args, **kwargs):
        serializer = ReviewValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data={'errors': serializer.errors},
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        text = serializer.validated_data.get('text')
        stars = serializer.validated_data.get('stars')
        movie_id = serializer.validated_data.get('movie_id')
        review_obj = Director.objects.create(text=text, stars=stars, movie_id=movie_id)
        return Response(data=ReviewSerializer(review_obj).data)


class ReviewDetailListApiView(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        review_obj = Review.objects.get(id=id)
        serializer = ReviewValidateSerializer(data=request.data)
        review_obj.text = serializer.validated_data.get('text')
        review_obj.stars = serializer.validated_data.get('stars')
        review_obj.movie_id = serializer.validated_data.get('movie_id')
        return Response(data=DirectorSerializer(review_obj).data)
