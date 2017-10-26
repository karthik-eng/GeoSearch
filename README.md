
=========
GeoSearch
=========

GeoSearch is a sample Django app that does search on dataset : http://download.geonames.org/export/dump/ file : cities1000.zip

Proximity Query
● Given a city ID X query for the k closest cities where closeness is measured
using an appropriately chosen measure of distance by latitude and longitude.
● (Optional) Support restricting the above query by country.
● Lexical Query
● Given an input word, return any cities that match that word
● (Optional) Support multiple words, treating each one independently (e.g. The
query "taco bell" would be treated as "taco" AND "bell")


Quick start
-----------

1) Add a new app to your django project.
   python manage.py GeoSearch

2) Copy all the files from this Repo to GeoSearch folder.

3) In Project settings.py
   a) Add GeoSearch to list of INSTALLED_APPS
	INSTALLED_APPS = [
    	'GeoSearch'
     	...]
   b) Under TEMPLATES I had to add :

        'DIRS': ['.'],

4) In Project urls.py

	from django.conf.urls import include, url
	urlpatterns = [
    		url(r'^geosearch/$', include('GeoSearch.urls')),
	]

5) Access the app : http://127.0.0.1:8000/geosearch/
