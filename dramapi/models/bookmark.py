from django.db import models
from django.contrib.auth.models import User


class Bookmark(models.Model):
    entry = models.ForeignKey(
        "Entry", on_delete=models.CASCADE, related_name='bookmarks')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='bookmarks')
