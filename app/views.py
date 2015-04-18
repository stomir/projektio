from urllib import quote_plus, unquote_plus

from django.shortcuts import render
from django.http import HttpResponse

from dbfun import *
from app.tasks import *


def index(request):
    all_cinemas = getCinemas()
    for c in all_cinemas:
        c['link_name'] = quote_plus(c['name'].encode('utf-8'))
        c['link_type'] = quote_plus(c['cinema_type'].encode('utf-8'))

    context = {
        'all_cinemas': all_cinemas,
    }
    return render(request, 'index.html', context)

def mapa(request):
    all_cinemas = getCinemas()
    for c in all_cinemas:
        c['link_name'] = quote_plus(c['name'].encode('utf-8'))
        c['link_type'] = quote_plus(c['cinema_type'].encode('utf-8'))

    context = {
        'all_cinemas': all_cinemas
    }
    return render(request, 'map.html', context)

def repertuar(request, c_type, what):
    all_cinemas = getCinemas()
    for c in all_cinemas:
        c['link_name'] = quote_plus(c['name'].encode('utf-8'))
        c['link_type'] = quote_plus(c['cinema_type'].encode('utf-8'))

    if c_type != all and what != 'all':
        name = unquote_plus(what.encode('utf-8')).decode('utf-8')
        cinema_type = unquote_plus(c_type.encode('utf-8')).decode('utf-8')
        cin = getByCinema(cinema_type, name)
        t_begin = ""
        t_end = "2016"
        shows = []
        for mv in cin['movies']:
            for time in mv['shows']:
                if t_begin <= time and time <= t_end:
                    shows.append({'date': time, 'title': mv['title'], 'name': name, 'address': cin['address']})
    else:
        name = "Wszystkie kina"
        cinema_type = ""
        shows = getShows()
        #shows = {}

    context = {
        'all_cinemas': all_cinemas,
        'name': name,
        'cinema_type': cinema_type,
        'shows': shows,
    }
    return render(request, 'repertuar.html', context)

def data_import(request):
    importData()
    return HttpResponse("Data imported.")