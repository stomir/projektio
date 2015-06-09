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
        Wszystkie kina

    ``all_movies``
        Wszystkie filmy

    **Template:**

        `index.html`

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

    **Argumenty:**

    ``movie``
        ID wybranego filmu

    ``day``
        Dzień: 0 - dziś, 1 - jutro, 2 - pojutrze

    **Context**

    ``all_cinemas``
        Wszystkie kina.

    ``cinemas``
        Kina do wyświetlenia na mapie.

    ``movie``
        Wybrany film.

    **Template:**

        `map.html`

    """
    all_cinemas = getCinemas()
    if movie and day:
        if day == "0":
            d1 = datetime.now()
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

    **Argumenty:**

    ``day``
        Dzień: 0 - dziś, 1 - jutro, 2 - pojutrze

    ``type``
        Typ biletu: 0 - normalny, 1 - ulgowy, 2 - studencki

    **Context**

    ``all_cinemas``
        Wszystkie kina.

    ``type``
        Typ biletu do wyświetlenia

    ``shows``
        Pokazy do wyświetlenia w repertuarze.

    ``name``
        Tytuł wyświetlanego repertuaru.

    **Template:**

        `repertuar.html`

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

    **Argumenty:**

    ``cinema``
        ID wybranego kina

    ``day``
        Dzień: 0 - dziś, 1 - jutro, 2 - pojutrze

    ``type``
        Typ biletu: 0 - normalny, 1 - ulgowy, 2 - studencki

    **Context**

    ``all_cinemas``
        Wszystkie kina.

    ``type``
        Typ biletu do wyświetlenia

    ``shows``
        Pokazy do wyświetlenia w repertuarze.

    ``name``
        Tytuł wyświetlanego repertuaru.

    **Template:**

        `repertuar.html`

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

    **Argumenty:**

    ``movie``
        ID wybranego filmu

    ``day``
        Dzień: 0 - dziś, 1 - jutro, 2 - pojutrze

    ``type``
        Typ biletu: 0 - normalny, 1 - ulgowy, 2 - studencki

    **Context**

    ``all_cinemas``
        Wszystkie kina.

    ``type``
        Typ biletu do wyświetlenia

    ``shows``
        Pokazy do wyświetlenia w repertuarze.

    ``name``
        Tytuł wyświetlanego repertuaru.

    **Template:**

        `repertuar.html`

    """
    all_cinemas = getCinemas()
    if day == "0":
        d1 = datetime.now()#pytz.timezone("Europe/Warsaw")) + timedelta(int(day))
    else:
        d1 = date.today() + timedelta(int(day))
    d2 = date.today() + timedelta(int(day) + 1)
    m = Movie.objects.get(id=movie)

    shows = getByMovie(m.title).filter(date__range=(d1, d2)).order_by("date")
    for s in shows:
        s.price = s.get_price_by_type(type)

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