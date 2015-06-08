from datetime import datetime, date, time
import threading

from django.utils import timezone
from app.models import Cinema, Movie, Show



#Aktualizacja bazy danych
def importData():

    from app.cinemacity  import getData
    data1 = getData()

    from app.multikino  import getData
    data2 = getData()

    if (len(data1) == 0 and len(data2) == 0) or (data1 == None and data2 == None):
        return None#wyslij info do admina

    Show.objects.all().delete()
    Movie.objects.all().delete()

    for t in range(1,3):

        if t == 1:
            data = data1
            from app.cinemacity  import getCinemaType
        else:
            data = data2
            from app.multikino  import getCinemaType

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

          #  prices = Price.objects.filter(cinema = cin)
            movies = i['movies']

            for m in movies:
                mov = Movie.objects.filter(title = m['title'])
                #Czy nowy film
                if len(mov) == 0:
                    mov = Movie(title = m['title'])
                    mov.save()
                else:
                    mov = mov[0]

                for s in m['shows']:

                    price = s['price']
                    show = Show(cinema = cin, movie = mov, normal = price['normal'] , student = price['student'], reduced = price['reduced'])

                    if t == 1:
                        show.date = datetime.strptime(s['time'], "%Y-%m-%d %H:%M")
                    else:
                        show.date = datetime.strptime(s['time'], "%Y-%m-%d %H:%M:%S")

                            #show.date = show.date.replace(tzinfo=pytz.timezone('Europe/Warsaw'))

                    show.save()


def importDaily():
    importData()
    threading.Timer(24*60*60, importDaily).start() # 1 dzien
