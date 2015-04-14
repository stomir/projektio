from .models import Cinema, Movie, Show
from django.db.models import Count

def getByMovie (title):

	cin = Cinema.objects.values('cinema_type', 'name', 'address', 'lat', 'lng')

	result = []
	
	for i in cin:
		i['shows'] = list(Show.objects.filter(movie__title = title, cinema__name = i['name']).values_list('date', flat = True))
		for j in  range(0, len(i['shows'])): 
			i['shows'][j] = i['shows'][j].strftime("%Y-%m-%d %H:%M")

		if len(i['shows']) > 0:
			result.append(i)
			 
	if len(result) == 0:
		return None
	else:
		return result



def getByCinema(cinema_type, name):

	result = Cinema.objects.filter(cinema_type=cinema_type, name=name).values('address', 'lat', 'lng')

	if len(result) == 0:
		return None

	result =  result[0]
	resultMovies = []
	mov = Movie.objects.values('title')
	
	for i in mov:
		i['shows'] = list (Show.objects.filter(movie__title = i['title'], cinema__name = name).values_list('date', flat = True))
		for j in  range(0, len(i['shows'])): 
			i['shows'][j] = i['shows'][j].strftime("%Y-%m-%d %H:%M")

		if len(i['shows']) > 0:
			resultMovies.append(i)
			 
	result['movies'] = resultMovies
	
	return result



def getCinemas():
	return Cinema.objects.values('cinema_type', 'name', 'address', 'lat', 'lng')

def getMovies():
	return Movie.objects.values_list('title', flat=True).order_by('title') 

def getShows():
        shows = Show.objects.all()
	result = []
	
	for show in  shows: 
		result.append({
				'title' : show.movie.title, 
				'cinema_type' : show.cinema.cinema_type,
				'name' : show.cinema.name,
				'address' : show.cinema.address,
				'lat' : show.cinema.lat,
				'lng' : show.cinema.lng,  	
				'date' : show.date.strftime("%Y-%m-%d %H:%M"),
		})

	return result
