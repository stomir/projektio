import urllib2;
import urllib;
import json;
import datetime;
from bs4 import BeautifulSoup;

google_api_key = 'AIzaSyBp4bRFYsAPL7ltefsD0f9nYIkby21At8o';

def clearTitle (title):
	title = title.replace(' 4DX', '');
	title = title.replace(' 3D', '');
	title = title.replace(' IMAX', '');
	title = title.replace(' / napisy', '');
	title = title.replace(' / dubbing', '');
	return title;

def resolveAddr (addr):
	json_data = urllib2.urlopen(("https://maps.googleapis.com/maps/api/geocode/json?"+urllib.urlencode({'address':addr,'key':google_api_key}))).read()
	data = json.loads(json_data).get('results')
	if (len(data) == 0):
		return False;
	data = {
		'lat' : data[0].get('geometry').get('location').get('lat'),
		'lng' : data[0].get('geometry').get('location').get('lng'),
	};
	return data;

def getCinemaType ():
	return "MultiKino";

def getReserveLink(addr, time, title):
	return "http://multikino.pl"

def myGetData():
	cinemas_html = urllib2.urlopen("http://multikino.pl/pl/wszystkie-kina").read()
	cinemas_json = urllib2.urlopen("http://multikino.pl/pl/repertoire/cinema/index").read()
	soup = BeautifulSoup(cinemas_html);
	iddict = {}
	ret = []
	for a in json.loads(cinemas_json)['results']:
		name = a['name']
		cinid = a['id'];
		iddict[name] = cinid;
	
	for cinema_soup in soup.find('div', {'id':'placeholder-main-plugin-1'}).children:
		if (cinema_soup.name == 'h3'):
			cinema_name = cinema_soup.find('strong').contents[0]
			cinema_id = iddict[cinema_name]
			cinema_addr = cinema_soup.findNext('p').contents[0].encode('utf-8').strip()
			cinema_location = resolveAddr(cinema_addr)
			if (not cinema_location):
				continue
			showdict = {}
			for i in range(0,7):
				dateiso = (datetime.date.today()+datetime.timedelta(i)).isoformat()
				schedule_json = urllib2.urlopen(("http://multikino.pl/pl/repertoire/cinema/seances?"+urllib.urlencode({'id':cinema_id,'from':dateiso}))).read()
				for a in json.loads(schedule_json)['results']:
					movie_title = clearTitle(a['title'])
					if (not movie_title in showdict):
						showdict[movie_title] = []
					for s in a['seances']:
						showdict[movie_title].append(s['beginning_date'])
			retmovies = []
			for title in showdict:
				retmovies.append({'title':title,'shows':showdict[title]});
			ret.append({
				'name' : cinema_name,
				'address' : cinema_addr,
				'lat' : cinema_location['lat'],
				'lng' : cinema_location['lng'],
				'movies' : retmovies
			});
	return ret

def getData():
	try:
		data = myGetData()
	except:
		return None
	return data
