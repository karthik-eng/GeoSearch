from django.conf.urls import url
from .views import ListCities 

list_cities_view_obj = ListCities()

urlpatterns = [
    url(r'^$', list_cities_view_obj.index),
]
