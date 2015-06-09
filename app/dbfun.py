# Encoding: utf-8

from .models import Cinema, Movie, Show

def getByMovie (title):
    """
    Funkcja zwracająca QuerySet filmów o danym tytule.

    **Argumenty:**

    ``title``
        tytuł filmu
    """
    return Show.objects.filter(movie__title = title)

	
def getByCinema(cinema_type, name):
    """
    Funkcja zwracająca QuerySet filmów wyświetlanych w danym kinie.

    **Argumenty:**

    ``cinema_type``
        Sieć kin
    ``name``
        Nazwa kina
    """
    return Show.objects.filter(cinema__cinema_type = cinema_type, cinema__name = name)

def getCinemas():
    """
    Funkcja zwracająca QuerySet wszystkich kin.
    """
    return Cinema.objects.all()

def getMovies():
    """
    Funkcja zwracająca QuerySet wszystkich filmów.
    """
    return Movie.objects.all()

def getShows(year, month, day):
    """
    Funkcja zwracająca QuerySet filmów z określonej daty.
    """
    return Show.objects.filter(date__year = year, date__month = month, date__day = day)
