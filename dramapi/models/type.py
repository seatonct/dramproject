from django.db import models


class Type(models.Model):
    label = models.CharField(max_length=300)
