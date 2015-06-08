import urllib2;
import urllib;
import json;
import datetime;
from bs4 import BeautifulSoup;

google_api_key = 'AIzaSyBp4bRFYsAPL7ltefsD0f9nYIkby21At8o';


def clearTitle(title):
    title = title.replace(' 4DX', '');
    title = title.replace(' 3D', '');
    title = title.replace(' IMAX', '');
    title = title.replace(' VIP', '');
    return title;


def resolveAddr(addr):
    json_data = urllib2.urlopen(("https://maps.googleapis.com/maps/api/geocode/json?" + urllib.urlencode(
        {'address': addr, 'key': google_api_key}))).read()
    data = json.loads(json_data).get('results')
    if (len(data) == 0):
        return False;
    data = {
        'lat': data[0].get('geometry').get('location').get('lat'),
        'lng': data[0].get('geometry').get('location').get('lng'),
    };
    return data;


def getCinemaType():
    return "CinemaCity";


def getReserveLink(addr, time, title):
    return "http://cinema-city.pl";


def myGetData():
    cinemas_html = urllib2.urlopen("http://cinema-city.pl/cinemas").read()
    soup = BeautifulSoup(cinemas_html);
    iddict = {}
    ret = []
    for a in soup.findAll('a', {'data-venue_type_id': 0}):
        name = a.contents[0].encode('utf-8')
        cinid = a['data-site_id'];
        iddict[name] = cinid;

    for cinema_soup in soup.findAll('table', {'class': 'cinema'}):
        a_soup = cinema_soup.find('div', {'class': 'cinema_name'}).find('a')
        name = a_soup.contents[0].encode('utf-8')
        name = name.replace(' Galeria', '')
        href = a_soup['href']
        addr = cinema_soup.find('td', {'class': 'cinema_info'}).findAll(text=True)
        addr = (addr[2].lstrip() + ' ' + addr[3].lstrip()).encode('utf-8')
        location = resolveAddr(addr)
        if (not location):
            continue;

        print name

        price_link = "http://cinema-city.pl/" + href
        price_soup = BeautifulSoup(urllib2.urlopen(price_link).read())

        price_table = price_soup.select("table.pricelist")[0]

        normal_row = price_table.select("tr:nth-of-type(2)")[0]
        reduced_row = price_table.select("tr:nth-of-type(3)")[0]
        student_row = price_table.select("tr:nth-of-type(5)")[0]

        p_everyday = {'normal': float(normal_row.select("td:nth-of-type(2)")[0].contents[0]),
                      'reduced': float(reduced_row.select("td:nth-of-type(2)")[0].contents[0]),
                      'student': float(student_row.select("td:nth-of-type(2)")[0].contents[0])}

        if (href != "Jurajska"):
            p_wed = {'normal': float(normal_row.select("td:nth-of-type(3)")[0].contents[0]),
                    'reduced': float(reduced_row.select("td:nth-of-type(3)")[0].contents[0]),
                    'student': float(student_row.select("td:nth-of-type(3)")[0].contents[0])}
        else:
            p_wed = {'normal': float(normal_row.select("td:nth-of-type(3)")[0].contents[0]),
                    'reduced': float(reduced_row.select("td:nth-of-type(3)")[0].contents[0]),
                    'student': float(student_row.select("td:nth-of-type(3) div")[0].contents[0])}

        p_weekend = {'normal': float(normal_row.select("td:nth-of-type(4)")[0].contents[0]),
                     'reduced': float(reduced_row.select("td:nth-of-type(4)")[0].contents[0]),
                     'student': float(student_row.select("td:nth-of-type(4)")[0].contents[0])}

        showdict = {}
        for i in range(0, 7):
            date = (datetime.date.today() + datetime.timedelta(i)).strftime('%d/%m/%Y')
            dateiso = (datetime.date.today() + datetime.timedelta(i)).isoformat()
            schedule_html = urllib2.urlopen(("http://cinema-city.pl/scheduleInfo?" + urllib.urlencode(
                {'locationId': iddict[name], 'date': date}))).read()
            schedule_soup = BeautifulSoup(schedule_html)
            for tr in schedule_soup.find('table', {'class': 'scheduleInfoTable'}).find('tbody').findAll('tr'):
                try:
                    title = tr.find('td', {'class': 'featureName'}).find('a').contents[0].encode('utf-8')
                except:
                    continue
                ctitle = clearTitle(title)
                if (not ctitle in showdict):
                    showdict[ctitle] = []
                shows = []
                for show in tr.findAll('a'):
                    time = show.contents[0].lstrip().rstrip().encode('utf-8')
                    if (time == title):
                        continue;

                    s_time = datetime.datetime.strptime((dateiso + ' ' + time).encode('utf-8'), "%Y-%m-%d %H:%M")

                    if s_time.isoweekday() > 5 or (s_time.isoweekday() == 5 and s_time.time() >= datetime.time(17, 00)):
                        p = p_weekend
                    elif s_time.isoweekday == 3:
                        p = p_wed
                    else:
                        p = p_everyday

                    showdict[ctitle].append({'time': (dateiso + ' ' + time).encode('utf-8'), 'price': p})
        retmovies = []
        for title in showdict:
            retmovies.append(
                {'title': title, 'shows': showdict[title], 'price': {'normal': 26, 'reduced': 19, 'student': 19}});
        ret.append({
            'name': name,
            'address': addr,
            'lat': location['lat'],
            'lng': location['lng'],
            'movies': retmovies
        });
    return ret


def getData():
    try:
        data = myGetData()
    except:
        return None
    return data
