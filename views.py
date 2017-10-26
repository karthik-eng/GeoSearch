# -*- coding: utf-8 -*-

import os

from django.http import JsonResponse
from django.shortcuts import render
from Geo import Geo

# Create your views here.
class ListCities(object):
    """
    View to execute the proximity and lexical queries and return json outputs
    """
    def __init__(self):
	dir_path = os.path.dirname(os.path.realpath(__file__))
    	self.geo_obj =  Geo(dir_path+'/cities_dump/cities1000.txt')

    def api(self, request):
	return self.index(request, api_mode=1)

    def index(self, request, api_mode=0):

	if request.method == 'POST':
		search_type=None
		lex_string = request.POST.get('lexical_search_string')
		proximity_city = request.POST.get('current_city')
		if lex_string:
			search_type = 'lexical'
			input_string = lex_string
		elif proximity_city:
			search_type = 'proximity'
			from_city_id = proximity_city
			filter_by_country = request.POST.get('country_check')
			k = request.POST.get('number_of_cities')
	if request.method == 'GET':
		search_type = None
		if api_mode == 1:
	 		search_type = request.GET['search_type']
			if search_type == 'lexical':
				input_string = request.GET['input_string']
			elif search_type == 'proximity':
				from_city_id = request.GET['from_city_id']
				k = request.GET['k']
				try:
					filter_by_country = request.GET['filter_by_country']
				except:
					filter_by_country = False

	dataset = self.geo_obj.dataset
	city_ids=[]
	if search_type == 'proximity':
	        req_json = {'search_type' : search_type, 'from_city_id' : from_city_id,'k' : k , 'filter_by_country': filter_by_country }
		nearest_city_ids = self.geo_obj.get_nearest_k_cities( 
                	   from_city_id, k=int(k), country_check=filter_by_country)
		city_ids = nearest_city_ids
	elif search_type == 'lexical':
		input_string = input_string.encode('utf-8')
		req_json = {'search_type' : search_type, 'input_string' : input_string}
		matching_city_ids = self.geo_obj.get_cities_lexical_match(input_string)
		city_ids = matching_city_ids

	output_l = []
	for city_id in city_ids:
		output_l.append(self.geo_obj.dataset[city_id])
	if api_mode == 1:
		return JsonResponse(output_l,safe=False)
	else:
        	return render(request, 'GeoSearch/templates/GeoSearch.html', {'output_l': output_l})


