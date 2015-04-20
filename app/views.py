from urllib import quote_plus, unquote_plus
from datetime import timedelta
from django.shortcuts import render
from django.http import HttpResponse
from django.utils.timezone import is_aware
from dbfun import *
from app.tasks import *


def index(request):
    all_cinemas = getCinemas()
    all_movies = getMovies()

    context = {
        'all_cinemas': all_cinemas,
        'all_movies': all_movies,
    }
    return render(request, 'index.html', context)


def mapa(request):
    all_cinemas = getCinemas()

    context = {
        'all_cinemas': all_cinemas
    }
    return render(request, 'map.html', context)


def repertuar(request, day="0"):
    all_cinemas = getCinemas()
    d = date.today() + timedelta(int(day))
    shows = getShows(d.year, d.month, d.day).order_by("date")

    context = {
        'shows': shows,
        'name': "Repertuar wszystkich kin",
        'all_cinemas': all_cinemas,
    }
    return render(request, 'repertuar.html', context)


def by_cinema(request, cinema, day="0"):
    all_cinemas = getCinemas()
    if day == "0":
        d1 = datetime.now(pytz.timezone("Europe/Warsaw")) + timedelta(int(day))
    else:
        d1 = datetime.today() + timedelta(int(day))
    d2 = d1 + timedelta(1)

    c = Cinema.objects.get(id=cinema)
    shows = getByCinema(c.cinema_type, c.name).filter(date__range=(d1, d2)).order_by("date")

    context = {
        'shows': shows,
        'name': "Repertuar dla kina " + c.cinema_type + " - " + c.name,
        'all_cinemas': all_cinemas,
    }
    return render(request, 'repertuar.html', context)


def by_movie(request, movie, day="0"):
    all_cinemas = getCinemas()
    if day == "0":
        d1 = datetime.now(pytz.timezone("Europe/Warsaw")) + timedelta(int(day))
    else:
        d1 = datetime.today() + timedelta(int(day))
    d2 = d1 + timedelta(1)
    m = Movie.objects.get(id=movie)
    print "Movies", d1, "-", d2
    shows = getByMovie(m.title).filter(date__range=(d1, d2)).order_by("date")
    for sh in shows:
        print sh.date
    context = {
        'shows': shows,
        'name': "Repertuar filmu \"" + m.title + "\"",
        'all_cinemas': all_cinemas,
    }
    return render(request, 'repertuar.html', context)


def data_import(request):
    importData()
    return HttpResponse("Data imported.")