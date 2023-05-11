from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Director, Movie, Review, Genre


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = 'id name movies_count movies_list'.split()


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = "id title genres description duration director_name".split()


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = 'id stars text movie_title'.split()


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = 'title rating reviews_text'.split()


class DirectorValidateSerializer(serializers.Serializer):
    name = serializers.CharField(min_length=1, max_length=100)


class MovieValidateSerializer(serializers.Serializer):
    title = serializers.CharField(min_length=1, max_length=100)
    duration = serializers.DurationField()
    description = serializers.CharField(required=False, default='No description')
    director_id = serializers.IntegerField()
    genres = serializers.ListField(child=serializers.IntegerField())

    def validate_genres(self, genres):
        genres_from_db = Genre.objects.filter(id__in=genres).values_list('id', flat=True)  # [1,2]
        if len(genres_from_db) != len(genres):
            raise ValidationError('Genre does not exist!')
        return genres  # collecting errors

    def validate_director_id(self, director_id):
        try:
            Director.objects.get(id=director_id)
        except Director.DoesNotExist:
            raise ValidationError(f"Error! {director_id} does not exists")
        return director_id


class ReviewValidateSerializer(serializers.Serializer):
    text = serializers.CharField(min_length=4, max_length=100)
    stars = serializers.IntegerField(min_value=1, max_value=5)
    movie_id = serializers.IntegerField()

    def validate_movie_id(self, movie_id):
        try:
            Review.objects.get(movie_id=movie_id)
        except Review.DoesNotExist:
            raise ValidationError('Movie not found!')
