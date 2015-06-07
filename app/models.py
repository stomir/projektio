# Encoding: utf-8

from django.db import models


class Cinema(models.Model):
    """
    Zawiera informacje o kinie.

    cinema_type - sieć, name - nazwa, address - adres, lat & lng - współrzędne geograficzne
    """
    cinema_type = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    lat = models.FloatField()
    lng = models.FloatField()


class Movie(models.Model):
    """
    Zawiera informacje o filmie

    title - tytuł
    """
    title = models.CharField(max_length=100)


class Show(models.Model):
    """
    Zawiera informacje o pokazie

    cinema - kino (:model:`app.Cinema`), movie - film (:model:`app.Movie`), date - data i czas pokazu
    """
    cinema = models.ForeignKey(Cinema)
    movie = models.ForeignKey(Movie)
    date = models.DateTimeField()


class Price(models.Model):
    cinema = models.ForeignKey(Cinema)
    movie = models.ForeignKey(Movie)
    normal = models.FloatField()
    student = models.FloatField()
    reduced = models.FloatField()

    def get_price_by_type(self, type):
        if type == "0":
            return self.normal
        elif type == "1":
            return self.reduced
        else:
            return self.student


