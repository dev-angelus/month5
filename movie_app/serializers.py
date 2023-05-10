from rest_framework import serializers
from .models import Director, Movie, Review


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = 'id name movies_count movies_list'.split()


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = "id title description duration director".split()


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = 'id stars text movie_title'.split()


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = 'title rating reviews_text'.split()