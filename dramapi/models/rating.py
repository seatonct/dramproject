from django.db import models


class Rating(models.Model):
    number_rating = models.IntegerField()
    label = models.CharField(max_length=10)
