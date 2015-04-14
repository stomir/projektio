from datetime import datetime, date, time
import threading
import pytz

from django.utils import timezone
from app.models import Cinema, Movie, Show
from app.cinemacity  import getData, getCinemaType

def importData():

	Show.objects.all().delete()
	Movie.objects.all().delete()

	data = getData()

	for i in data:

		cin = Cinema.objects.filter(name = i['name'])

		#Czy nowe kino
		if len(cin) == 0: 
			cin = Cinema(
				name = i['name'],
				cinema_type = getCinemaType(), 
				address = i['address'], 
				lat = i['lat'], 
				lng = i['lng']
			)
			cin.save()
		else:
			cin = cin[0]


		movies = i['movies']

		for m in movies:
			mov = Movie.objects.filter(title = m['title'])
			if len(mov) == 0:
        	                mov = Movie(title = m['title'])
				mov.save()
                	else:
                       		mov = mov[0]
			
			for s in m['shows']:
				show = Show(cinema = cin, movie = mov, date = datetime.strptime(s, "%Y-%m-%d %H:%M"))
			 	show.date = show.date.replace(tzinfo=pytz.timezone('Europe/Warsaw'))

				show.save()


def importWeekly():
	importData()	
	threading.Timer(604800, importWeekly).start()
