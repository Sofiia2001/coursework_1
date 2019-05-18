import geocoder
import sqlite3
import json
from tqdm import tqdm


class TweetsByCountries:
    '''
    Abstract data type that gives an opportunity
    to make actions with data from twitter posts
    '''

    def __init__(self, data_base):
        '''
        Initializes data base name and creates empty dictionary to store data

        :param data_base: string name of data base to use
        '''
        with open('tweets_amount.json') as file:
            self.tweets_amount_by_countries = json.load(file)
            self.current_position = self.tweets_amount_by_countries['CURRENT_POSITION']

        if data_base.endswith('.db'):
            self.data_base = data_base

    def _get_locations(self):
        '''
        Internal method to get locations from tweets data base

        :return: list of locations
        '''
        connection = sqlite3.connect(self.data_base)
        cursor = connection.cursor()

        locations = """SELECT location FROM TWITTER"""
        cursor.execute(locations)

        result = cursor.fetchall()
        return result

    def clean_locations(self):
        '''
        Additional method to clean locations, that means to make locations
        more readable and make them fitting the library

        :return: list with cleared locations
        '''
        locations = self._get_locations()
        cleared_locations = []

        for location in locations:
            location = location[0].replace(': ', '').replace('\n', '')
            if ',' in location: location = location[:location.index(',')]

            cleared_locations.append(location)

        return cleared_locations

    def tweets_amount_geonames(self):
        '''
        Method to get amount of tweets in certain countries using geonames

        Unfortunately, works with a limited amount of requests, so be careful
        using it in your code.
        It has approximately 1000 requests available in one hour

        :return: dictionary of a look {'country': num_of_tweets}
        '''
        cleared_locations = self.clean_locations()

        for loc in cleared_locations:
            g = geocoder.geonames(loc, key='sofiiatatosh')
            if g.country in self.tweets_amount_by_countries:
                self.tweets_amount_by_countries[g.country] += 1
            else:
                self.tweets_amount_by_countries[g.country] = 1

        return self.tweets_amount_by_countries

    def _check_existance(self, res):
        if res in self.tweets_amount_by_countries:
            self.tweets_amount_by_countries[res] += 1
        else:
            self.tweets_amount_by_countries[res] = 1

    def tweets_amount_db(self):
        '''
        A method that uses both database with all the cities in various countries
        and makes requests on geonames to later count suicidal post on Twitter
        dividing the amount on location by countries

        :return: dictionary of a look {'country': num_of_tweets}
        '''
        cleared_locations = self.clean_locations()

        counter = 19

        with sqlite3.connect('Cities_data.db') as connection:
            cursor = connection.cursor()

            for loc in tqdm(range(self.current_position, self.current_position + counter)):
                # counter -= 1
                select = "SELECT country_name FROM CITIES WHERE city=?"
                cursor.execute(select, [(cleared_locations[loc])])
                res = cursor.fetchall()

                if res:
                    if len(res) > 1:
                        try:
                            g = geocoder.geonames(loc, key='sofiiatatosh')
                            res = g.country
                        except:
                            res = res[0][0]

                    elif len(res) == 1:
                        res = res[0][0]

                    self._check_existance(res)
                self.tweets_amount_by_countries['CURRENT_POSITION'] += 1
                    # print(self.current_position)

        return self.tweets_amount_by_countries

    def get_amount_in_country(self, country):
        '''
        Returns amount of suicidal tweets  in a given country if
        this country exists in dictionary data storage

        :param country: name of a country in a string form
        :return: int, the amount of posts in a given country
        '''
        if country in self.tweets_amount_by_countries:
            return self.tweets_amount_by_countries[country]

    def write_into_file(self):
        '''
        Writes data into a json file to store it because
        of a limitation of requests

        :return:
        '''
        data = self.tweets_amount_db()
        with open('tweets_amount.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False)


def initial_file():
    '''
    A method to create initial file view

    :return:
    '''
    with open('tweets_amount.json', 'w', encoding='utf-8') as file:
        json.dump({'CURRENT_POSITION': 0}, file, ensure_ascii=False)