from django.db import models


class Color(models.Model):
    label = models.CharField(max_length=300)
    color_grade = models.DecimalField(max_digits=3, decimal_places=1)
    hex_code = models.CharField(max_length=6)
    tailwind_name = models.CharField(max_length=155)
