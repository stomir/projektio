# Znajdź mi kino
Tworzony przez nas system “Znajdź mi kino” służy do szybkiego i prostego przeglądania 
oferty najbliższych kin. Dzięki naszej aplikacji można dowiedzieć się o godzinach seansów, 
cenach biletów oraz sposobie i czasie dojazdu do kina. Bezpośrednio z niej można się dostać 
do rezerwacji internetowej biletów w wybranym kinie.

# Paczka instalacyjna
Do instalacji paczki wymagane sa następujące moduły:
  django
  BeautifulSoup4
  pytz
Należy ustawić SECRET_KEY w pliku Znajdz_Mi_Kino/settings.py
Następnie należy uruchomić następujące komendy:
  manage.py migrate
  manage.py dbupdate& -- To moze chwilę potrwać
  manage.py runserver 0.0.0.0:80
