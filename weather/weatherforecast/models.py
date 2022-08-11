from django.db import models
from django.urls import reverse


class RegionsModel(models.Model):
    regName = models.CharField(max_length=100, verbose_name='region')
    type = models.CharField(max_length=50, verbose_name='type')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='slug')

    def __str__(self):
        return self.regName

    def get_absolute_url(self):
        return reverse('region', kwargs={'reg_slug': self.slug})


class CitiesModel(models.Model):
    cityName = models.CharField(max_length=100, verbose_name='City')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='slug')
    lat = models.FloatField(verbose_name='latitude')
    lon = models.FloatField(verbose_name='longitude')
    reg = models.ForeignKey('RegionsModel', on_delete=models.CASCADE, verbose_name='region')

    def __str__(self):
        return self.cityName

    def get_absolute_url(self):
        return reverse('city_now', kwargs={'city_slug': self.slug})