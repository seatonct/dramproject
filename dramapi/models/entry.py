from django.contrib.auth.models import User
from django.db import models


class Entry(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_entry')
    whiskey = models.CharField(max_length=155)
    whiskey_type = models.ForeignKey(
        "Type", on_delete=models.CASCADE, related_name='entry_type')
    country = models.CharField(max_length=155)
    part_of_country = models.CharField(max_length=155, blank=True, null=True)
    age_in_years = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True)
    proof = models.DecimalField(max_digits=6, decimal_places=2)
    color = models.ForeignKey(
        "Color", on_delete=models.CASCADE, related_name='entry_color', blank=True, null=True)
    mash_bill = models.CharField(max_length=155, blank=True, null=True)
    maturation_details = models.CharField(
        max_length=300, blank=True, null=True)
    nose = models.CharField(max_length=300)
    palate = models.CharField(max_length=300)
    finish = models.CharField(max_length=300, blank=True, null=True)
    rating = models.ForeignKey(
        "Rating", on_delete=models.CASCADE, related_name='entry_rating')
    notes = models.CharField(max_length=1000, blank=True, null=True)
    publication_date = models.DateField(auto_now_add=True)
    image_url = models.CharField(max_length=300, blank=True, null=True)
    published = models.BooleanField(default=False)
