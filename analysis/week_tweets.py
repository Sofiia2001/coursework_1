import sqlite3
import datetime
from tqdm import tqdm
import geocoder
import json
import os


dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


class WeekTweets:
    def __init__(self, date=''):
        '''
        Asks user to input a date of a week to form a whole week
        '''
        self.date = date
        self._week_list = []
        self._tweets_week_dict = {}
        # self.num_of_tweets = {}

    def select_week(self):
        '''
        Creates a week due to a correct calendar

        :return: None   
        '''
        try:
            date = datetime.datetime(2019, int(self.date[3:]), int(self.date[:2]))
            for i in range(date.weekday(), 0, -1):
                self._week_list.append((date - datetime.timedelta(days=i)).strftime('%Y-%m-%d'))
            self._week_list.append(date.strftime('%Y-%m-%d'))
            for j in range(1, 7 - date.weekday()):
                self._week_list.append((date + datetime.timedelta(days=j)).strftime('%Y-%m-%d'))
        except:
            return 'This date does not exist'

    def tweets_for_week(self):
        '''
        Collects all the tweets from a gathered database in weekdays formed before

        :return: dictionary with date: tweets made in that day
        '''
        self.select_week()
        with sqlite3.connect(f'{dir_path}/data/Twitter_data.db') as connection:
            cursor = connection.cursor()

            for w in self._week_list:

                select = "SELECT * FROM TWITTER WHERE created_at LIKE ?"

                cursor.execute(select, [(f'%{w}%')])
                res = cursor.fetchall()
                self._tweets_week_dict[w] = len(res)

    def find_week_day(self):
        '''
        Finds week day when the biggest number of tweets was posted

        :return: max week day of a week
        '''
        maxx = max(self._tweets_week_dict.values())
        for i in self._tweets_week_dict:
            if self._tweets_week_dict[i] == maxx:
                key = i.split('-')
                date = datetime.datetime(int(key[0]), int(key[1]), int(key[2]))
        return date.strftime('%A')

    def _tweets_for_week_day(self):
        '''
        Returns number of tweets on a certain day

        :return: amount of tweets on mondays(eg)
        '''
        # day = input('Please, choose a week day you want to analyze\n'
                    # '[mon/tue/wed/thu/fri/sat/sun]: ')

        weekdays = {
            'mon': 'Monday',
            'tue': 'Tuesday',
            'wed': 'Wednesday',
            'thu': 'Thursday',
            'fri': 'Friday',
            'sat': 'Saturday',
            'sun': 'Sunday'
        }

        num_of_tweets = {v: {'general': 0, 'dates': set(), 'posts': {}} for v in weekdays.values()}

        with sqlite3.connect(f'{dir_path}/data/Twitter_data.db') as connection:
            cursor = connection.cursor()

            select = "SELECT created_at FROM TWITTER"
            cursor.execute(select)
            res = cursor.fetchall()

            res = [date[0].replace(': ', '').strip() for date in res]
            for date in res:
                d = date[:date.index(' ')]
                splitted = d.split('-')
                day = datetime.datetime(int(splitted[0]), int(splitted[1]), int(splitted[2])).strftime('%A')

                if day in num_of_tweets:
                    num_of_tweets[day]['general'] += 1
                    num_of_tweets[day]['dates'].add(d)
        return num_of_tweets

    def tweets_by_countries_on_day(self):
        '''
        Returns number of tweets on a certain day from different countries

        :return: amount of tweets on mondays(eg)
        '''
        num_of_tweets = self._tweets_for_week_day()
        with sqlite3.connect('Twitter_data.db') as connection:
            cursor = connection.cursor()

            user_day = 'Sunday' #only as example
            locations = []
            countries = {}
            for u_date in num_of_tweets[user_day]['dates']:
                selection = "SELECT * FROM TWITTER WHERE created_at LIKE ?"
                cr_at = f'%{u_date}%'
                cursor.execute(selection, [(cr_at)])

                posts = cursor.fetchall()
                for p in posts:
                    if 'No location' not in p[3]: locations.append(p[3].replace(': ', '').strip())

                num_of_tweets[user_day]['posts'][u_date] = posts

            with sqlite3.connect('Cities_data.db') as connect:
                for loc in locations:
                    if ',' in loc: loc = loc[:loc.index(',')]
                    cursor_1 = connect.cursor()

                    select = "SELECT country_name FROM CITIES WHERE city=?"
                    cursor_1.execute(select, [(loc)])
                    print(loc)
                    res = cursor.fetchall()
                    # print(res)

                    try:
                        geo = geocoder.geonames(loc, key='sofiiatatosh')
                        country = geo.country
                    except:
                        country = res[0][0]

                    countries[country] = countries.get(country, 0)
                    countries[country] += 1

        return countries

    def maximum_tweets_day(self):
        '''
        Returns a day when there was the majority of suicide tweets posted
        '''
        to_return = ''
        num_of_tweets = self._tweets_for_week_day()
        maxx = max([v['general'] for v in num_of_tweets.values()])
        for day in num_of_tweets:
            if num_of_tweets[day]['general'] == maxx:
                to_return = day
        return to_return

    def write_daily_report_json(self):
        '''
        Write into json

        :return:
        '''
        data = self.tweets_by_countries_on_day()
        with open('daily_reports.json', 'w+', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False)


if __name__ == '__main__':
    week = WeekTweets()
    # week.write_daily_report_json()
    # data = self.tweets_by_countries_on_day()
    # data = {'Monday': {'Netherlands': 10, None: 600, 'India': 144, 'United Kingdom': 153, 'United States': 435, 'France': 60,
    #  'Australia': 76, 'Canada': 71, 'Jamaica': 7, 'Belgium': 4, 'Colombia': 1, 'Philippines': 5, 'Puerto Rico': 3,
    #  'New Zealand': 3, 'Belize': 1, 'Saudi Arabia': 1, 'Uruguay': 1, 'South Africa': 6, 'Ireland': 4, 'Seychelles': 6,
    #  'Antarctica': 3, 'Brazil': 5, 'Bonaire': 2, 'Trinidad and Tobago': 1, 'Zimbabwe': 2, 'Somalia': 3, 'Nigeria': 6,
    #  'Indonesia': 3, 'Taiwan': 1, 'Tanzania': 4, 'Peru': 1, 'Argentina': 3, 'Paraguay': 1, 'Costa Rica': 1,
    #  'Antigua and Barbuda': 1, 'Bangladesh': 1, 'Pakistan': 6, 'Georgia': 3, 'Kenya': 3, 'Sri Lanka': 2, 'China': 2,
    #  'Portugal': 1, 'Afghanistan': 1, 'Guatemala': 1, 'Qatar': 1, 'United Arab Emirates': 8, 'North Korea': 2,
    #  'Madagascar': 1, 'Romania': 1, 'Switzerland': 1, 'Germany': 6, 'Papua New Guinea': 1, 'Cayman Islands': 3,
    #  'Ethiopia': 1, 'Ecuador': 1, 'Mauritania': 2, 'Ghana': 2, 'Norfolk Island': 1, 'Kuwait': 2, 'Bahamas': 1,
    #  'Cameroon': 1, 'Thailand': 2, 'Spain': 3, 'Turkey': 1, 'Japan': 1, 'Italy': 2, 'Lebanon': 2,
    #  'Heard Island and McDonald Islands': 1, 'Greece': 1, 'Senegal': 1, 'Russia': 1, 'Iran': 1, 'Réunion': 3,
    #  'Bolivia': 1, 'Austria': 1, 'U.S. Virgin Islands': 3, 'Haiti': 1}}
    # with open('daily_reports.json', 'w+', encoding='utf-8') as file:
    #     json.dump(data, file, ensure_ascii=False)
