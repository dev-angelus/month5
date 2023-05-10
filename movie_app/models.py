from django.db import models


class Director(models.Model):
    name = models.CharField(max_length=100)

    @property
    def movies_count(self):
        return self.movie_set.count()

    def movies_list(self):
        return [movie.title for movie in self.movie_set.all()]

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    duration = models.DurationField()
    director = models.ForeignKey(Director, on_delete=models.CASCADE)

    @property
    def rating(self):
        stars_list = [review.stars for review in self.reviews.all()]
        return round(sum(stars_list) / len(stars_list), 2)

    @property
    def reviews_text(self):
        review_text = [review.text for review in self.reviews.all()]
        return review_text

    def __str__(self):
        return self.title


class Review(models.Model):
    CHOICES = ((i, "*" * i) for i in range(1, 6))
    text = models.TextField(blank=True, null=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    stars = models.IntegerField(choices=CHOICES, default=0)

    def __str__(self):
        return self.text

    @property
    def movie_title(self):
        return self.movie.title
