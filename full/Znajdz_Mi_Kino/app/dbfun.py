from .models import Cinema, Movie, Show

def getByMovie (title):

	return Show.objects.filter(movie__title = title)
#	cin = Cinema.objects.values('cinema_type', 'name', 'address', 'lat', 'lng')
#
#	result = []
#	
#	for i in cin:
#		i['shows'] = list(Show.objects.filter(movie__title = title, cinema__name = i['name']).values_list('date', flat = True))
#		for j in  range(0, len(i['shows'])): 
#			i['shows'][j] = i['shows'][j].strftime("%Y-%m-%d %H:%M")
#
#		if len(i['shows']) > 0:
#			result.append(i)
#			 
#	if len(result) == 0:
#		return None
#	else:
#		return result


	


def getByCinema(cinema_type, name):

	return Show.objects.filter(cinema__cinema_type = cinema_type, cinema__name = name)
#	result = Cinema.objects.filter(cinema_type=cinema_type, name=name).values('address', 'lat', 'lng')
#
#	if len(result) == 0:
#		return None
#
#	result =  result[0]
#	resultMovies = []
#	mov = Movie.objects.values('title')
#	
#	for i in mov:
#		i['shows'] = list (Show.objects.filter(movie__title = i['title'], cinema__name = name).values_list('date', flat = True))
#		for j in  range(0, len(i['shows'])): 
#			i['shows'][j] = i['shows'][j].strftime("%Y-%m-%d %H:%M")
#
#		if len(i['shows']) > 0:
#			resultMovies.append(i)
#			 
#	result['movies'] = resultMovies	
#	return result


def getCinemas():
	return Cinema.objects.all()

def getMovies():
	return Movie.objects.all() 

def getShows(year, month, day):
	return Show.objects.filter(date__year = year, date__month = month, date__day = day)
