# Encoding: utf-8
from datetime import timedelta
from django.shortcuts import render, redirect
from django.http import HttpResponse
from dbfun import *
from app.tasks import *
from models import *
import pytz


def index(request):
    """
    Widok strony głównej.

    **Context**

    ``all_cinemas``
        Wszystkie kina - :model:`app.Cinema`.

    ``all_movies``
        Wszystkie filmy - :model:`app.Movie`.

    **Template:**

    :template:`index.html`

    """
    if request.method == "POST":
        if "mapa" in request.POST:
            return redirect("mapa", movie=request.POST["movie"], day=request.POST["date"])
        elif "repertuar" in request.POST:
            return redirect("by_movie", movie=request.POST["movie"], day=request.POST["date"], type=request.POST["type"])
    else:
        all_cinemas = getCinemas()
        all_movies = getMovies().order_by("title")

        context = {
            'all_cinemas': all_cinemas,
            'all_movies': all_movies,
        }
        return render(request, 'index.html', context)


def mapa(request, movie="", day=""):
    """
    Widok pokazujący mapę kin wyświetlających wybrany film w danym dniu.

    **Context**

    ``all_cinemas``
        Wszystkie kina - :model:`app.Cinema`.

    ``cinemas``
        Kina (:model:`app.Cinema`) do wyświetlenia na mapie.

    ``movie``
        Wybrany film - :model:`app.Movie`.

    **Template:**

    :template:`map.html`

    """
    all_cinemas = getCinemas()
    if movie and day:
        if day == "0":
            d1 = datetime.now()#pytz.timezone("Europe/Warsaw")) + timedelta(int(day))
        else:
            d1 = date.today() + timedelta(int(day))
        d2 = date.today() + timedelta(int(day) + 1)

        m = Movie.objects.get(id=movie)
        shows = getByMovie(m.title).filter(date__range=(d1, d2)).order_by("date")
        cinemas = Cinema.objects.filter(id__in=shows.values("cinema"))
        for c in cinemas:
            c.shows = shows.filter(cinema=c)
    else:
        cinemas = all_cinemas
        m = ""

    context = {
        'all_cinemas': all_cinemas,
        'cinemas': cinemas,
        'movie': m
    }
    return render(request, 'map.html', context)


def repertuar(request, day="0", type="0"):
    """
    Widok pokazujący repertuar wszystkich kin w danym dniu.

    **Context**

    ``all_cinemas``
        Wszystkie kina - :model:`app.Cinema`.

    ``type``
        Typ biletu do wyświetlenia

    ``shows``
        Pokazy (:model:`app.Show`) do wyświetlenia w repertuarze.

    ``name``
        Tytuł wyświetlanego repertuaru.

    **Template:**

    :template:`repertuar.html`

    """
    all_cinemas = getCinemas()
    if day == "0":
        d = datetime.now()#pytz.timezone("Europe/Warsaw")) + timedelta(int(day))
    else:
        d = date.today() + timedelta(int(day))

    shows = getShows(d.year, d.month, d.day).order_by("date")
    for s in shows:
        s.price = s.get_price_by_type(type)

    context = {
        'type' : type,
        'shows': shows,
        'name': "Repertuar wszystkich kin",
        'all_cinemas': all_cinemas,
    }
    return render(request, 'repertuar.html', context)


def by_cinema(request, cinema, day="0", type="0"):
    """
    Widok pokazujący repertuar repertuar wybranego kina w określony dzień.

    **Context**

    ``all_cinemas``
        Wszystkie kina - :model:`app.Cinema`.

    ``type``
        Typ biletu do wyświetlenia

    ``shows``
        Pokazy (:model:`app.Show`) do wyświetlenia w repertuarze.

    ``name``
        Tytuł wyświetlanego repertuaru.

    **Template:**

    :template:`repertuar.html`

    """
    all_cinemas = getCinemas()
    if day == "0":
        d1 = datetime.now()#pytz.timezone("Europe/Warsaw")) + timedelta(int(day))
    else:
        d1 = date.today() + timedelta(int(day))
    d2 = date.today() + timedelta(int(day) + 1)

    c = Cinema.objects.get(id=cinema)
    shows = getByCinema(c.cinema_type, c.name).filter(date__range=(d1, d2)).order_by("date")

    for s in shows:
        s.price = s.get_price_by_type(type)

    context = {
        'type' : type,
        'shows': shows,
        'name': "Repertuar dla kina " + c.cinema_type + " - " + c.name,
        'all_cinemas': all_cinemas,
    }
    return render(request, 'repertuar.html', context)


def by_movie(request, movie, day="0", type="0"):
    """
    Widok pokazujący repertuar wybranego filmu w określony dzień we wszystkich kinach.

    **Context**

    ``all_cinemas``
        Wszystkie kina - :model:`app.Cinema`.

    ``type``
        Typ biletu do wyświetlenia

    ``shows``
        Pokazy (:model:`app.Show`) do wyświetlenia w repertuarze.

    ``name``
        Tytuł wyświetlanego repertuaru.

    **Template:**

    :template:`repertuar.html`

    """
    all_cinemas = getCinemas()
    if day == "0":
        d1 = datetime.now()#pytz.timezone("Europe/Warsaw")) + timedelta(int(day))
    else:
        d1 = date.today() + timedelta(int(day))
    d2 = date.today() + timedelta(int(day) + 1)
    m = Movie.objects.get(id=movie)
    print "Movies", d1, "-", d2
    shows = getByMovie(m.title).filter(date__range=(d1, d2)).order_by("date")
    for s in shows:
        s.price = s.get_price_by_type(type)

    for sh in shows:
        print sh.date
    context = {
        'type' : type,
        'shows': shows,
        'name': "Repertuar filmu \"" + m.title + "\"",
        'all_cinemas': all_cinemas,
    }
    return render(request, 'repertuar.html', context)


def data_import(request):
    importData()
    return HttpResponse("Data imported.")