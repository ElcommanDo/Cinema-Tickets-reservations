from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# Guest -- Movie -- Reservation


class Movie(models.Model):
    hall = models.CharField(max_length=10)
    movie_name = models.CharField(max_length=100)
    date = models.DateTimeField()

    def __str__(self):
        return self.movie_name


class Guest(models.Model):
    guest_name = models.CharField(max_length=120)
    guest_mobile = models.CharField(max_length=20)


class Reservation(models.Model):
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE,
                              related_name='reservation')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE,
                              related_name='reservation')


class Post(models.Model):
    title = models.CharField(max_length=120)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()

    def __str__(self):
        return self.title

