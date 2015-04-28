from .models import Cinema, Movie, Show

def getByMovie (title):
	return Show.objects.filter(movie__title = title)

	
def getByCinema(cinema_type, name):
	return Show.objects.filter(cinema__cinema_type = cinema_type, cinema__name = name)

def getCinemas():
	return Cinema.objects.all()

def getMovies():
	return Movie.objects.all() 

def getShows(year, month, day):
	return Show.objects.filter(date__year = year, date__month = month, date__day = day)
