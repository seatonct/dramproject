# Generated by Django 5.0 on 2023-12-06 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dramapi', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=300)),
                ('color_grade', models.DecimalField(decimal_places=1, max_digits=3)),
                ('hex_code', models.CharField(max_length=6)),
            ],
        ),
    ]