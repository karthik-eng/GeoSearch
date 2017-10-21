import math


class Geo(object):

    def __init__(self, file_name):
        self.file_name = file_name
        self.dataset = self._read_file(file_name)
	self.unique_words = self._get_unique_words_dict()
	self.nearest_cities_by_dist= {}

    def _read_file(self, file_name):
        column_l = [
            'geonameid',
            'name',
            'asciiname',
            'alternatenames',
            'latitude',
            'longitude',
            'feature class',
            'feature code',
            'country code',
            'cc2',
            'admin1 code',
            'admin2 code',
            'admin3 code',
            'admin4 code',
            'population',
            'elevation',
            'dem',
            'timezone',
            'modification date']
        self.dataset = {}
        file_obj = open(file_name, 'r')
        lines = file_obj.readlines()
        for line in lines:
            line_d = {}
            geo_records = line.split('\t')
            assert len(geo_records) == len(
                column_l), "Investigate: The line doesn't have sufficient data ?"
            for (idx, record) in enumerate(geo_records):
                line_d[column_l[idx]] = record
            self.dataset[geo_records[0]] = line_d
        return self.dataset

    def _get_unique_words_dict(self):
        """
                indexes unique words across name, asciiname, alternatenames
        """
        unique_words = {}
        for city_id in self.dataset.keys():
            # alternatenames
            name_l = self.dataset[city_id]["alternatenames"].split(',')
            # name
            name = self.dataset[city_id]["name"]
            name_l.append(name)
            # asciiname
            asciiname = self.dataset[city_id]["asciiname"]
            name_l.append(asciiname)
            for name in set(name_l):
                for word in name.lower().split():
                    try:
                        unique_words[word].add(city_id)
                    except KeyError as e:
                        unique_words[word] = set([city_id])
        return unique_words

    def get_nearest_k_cities(self, from_city_id, k, country_check=False):
        to_city_ids = self.dataset.keys()
        to_city_ids.remove(from_city_id)
        if k >= len(to_city_ids):
            return "we do not have %s cities nearest to your current city"
        if from_city_id not in self.nearest_cities_by_dist.keys():
            self.nearest_cities_by_dist[from_city_id] = {}
            for to_city_id in to_city_ids:
                dist = self._get_distance(from_city_id, to_city_id)
                if dist in self.nearest_cities_by_dist.keys():
                    self.nearest_cities_by_dist[from_city_id][dist].append(
                        to_city_id)
                else:
                    self.nearest_cities_by_dist[from_city_id][dist] = [
                        to_city_id]

        #  Get k city ids with least distance
        k_cities = []
        for dist in sorted(self.nearest_cities_by_dist[from_city_id].keys()):
            for city in self.nearest_cities_by_dist[from_city_id][dist]:
                if len(k_cities) < k:
                    if country_check:
                        if self.dataset[from_city_id]['country code'] == self.dataset[city]['country code']:
                            k_cities.append(city)
                    else:
                        k_cities.append(city)
                else:
                    return k_cities

    def _get_distance(self, from_city_id, to_city_id):
        # from cordinates
        x1 = float(self.dataset[from_city_id]['latitude'])
        y1 = float(self.dataset[from_city_id]['longitude'])
        # to cordinates
        x2 = float(self.dataset[to_city_id]['latitude'])
        y2 = float(self.dataset[to_city_id]['longitude'])
        distance = math.sqrt(math.pow((x2 - x1), 2) +
                             math.pow((y2 - y1), 2))
        #distance = round(distance,8)
        return distance

    def get_cities_lexical_match(self, words_string):
        words = words_string.strip().lower().split()
        if not words:
            return set()
        out_set = set()
        for word in words:
            if out_set:
                # set intersection & is diffrent than and
                out_set = out_set & self.unique_words[word]
            else:
                out_set = self.unique_words[word]
        return out_set


'''Tests'''
import unittest
from pprint import pformat
import random


class GeoUnitTest(unittest.TestCase):

    def test_proximity(self):
        '''Proximity'''
        geo_obj = Geo("cities1000.txt")
        cities_d = geo_obj.dataset
        all_cities_ids = cities_d.keys()

        for i in range(5):
            # for my_city_id in all_cities_ids:
            my_city_id = random.choice(all_cities_ids)
            print "\nCurrent city: %s " % cities_d[my_city_id]['name']
            min_range = 3
            max_range = 11
            sample_size = random.choice(range(1, 6))
            # max_range = len(all_cities_ids)
            for max_cities in random.sample(
                    range(min_range, max_range), sample_size):
                value_for_k = max_cities
                check_country_value = random.choice([True, False])
                # check_country_value=True
                print "Input : %s k: %s country_check: %s" % (my_city_id, value_for_k, check_country_value)
                nearest_city_ids = geo_obj.get_nearest_k_cities(
                    my_city_id, k=value_for_k, country_check=check_country_value)
                if nearest_city_ids:
                    i = 1
                    for id in nearest_city_ids:
                        distance = geo_obj._get_distance(my_city_id, id)
                        country = geo_obj.dataset[id]["country code"]
                        print "Nearest %s city %s of %s at %s in country %s " % (cities_d[id]['name'], i, value_for_k, distance, country)
                        i += 1
                else:
                    print pformat(geo_obj.nearest_cities_by_dist[my_city_id])
                    if value_for_k:
                        print "Lone city : No nearest %s cities for city %s with country check %s " % (max_cities, my_city_id, check_country_value)
                    else:
                        assert False, "No nearest %s cities for city %s with country check %s " % (
                            max_cities, my_city_id, check_country_value)

    def test_lexical(self):
        '''Lexical Search'''
        geo_obj = Geo("cities15000.txt")
        cities_d = geo_obj.dataset
        all_cities_ids = cities_d.keys()

        for i in range(10):
            my_city_id = random.choice(all_cities_ids)
            name_l = cities_d[my_city_id]["alternatenames"].split(',')
            name_l.append(cities_d[my_city_id]["asciiname"])
            name_l.append(cities_d[my_city_id]["name"])

            print my_city_id
            for name in name_l:
                name = random.choice([name.lower(), name.upper(), name])
                print "\nInput city: %s " % name
                matching_city_ids = geo_obj.get_cities_lexical_match(name)
                if name:
                    assert matching_city_ids
                    for city_id in matching_city_ids:
                        print "Matching city name : %s, asciiname: %s, alternatenames : %s" \
                            % (cities_d[city_id]["name"], cities_d[city_id]["asciiname"], cities_d[city_id]["alternatenames"])

            all_words = []
            for name in name_l:
                all_words = all_words + name.split()

            name = ' '.join(
                random.sample(
                    all_words,
                    random.choice(
                        range(
                            1,
                            3))))
            print "\nInput city: %s " % name
            matching_city_ids = geo_obj.get_cities_lexical_match(name)
            if name:
                assert matching_city_ids
                for city_id in matching_city_ids:
                    print "Matching city name : %s, asciiname: %s, alternatenames : %s" \
                        % (cities_d[city_id]["name"], cities_d[city_id]["asciiname"], cities_d[city_id]["alternatenames"])

suite = unittest.TestLoader().loadTestsFromTestCase(GeoUnitTest)
unittest.TextTestRunner(verbosity=4).run(suite)
