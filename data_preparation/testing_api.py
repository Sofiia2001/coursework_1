import tweepy
from hidden import credentials # hidden module cannot be posted on Github in terms of privacy policy
import json
import csv
import time
import sqlite3


def getting_data(consumer_token, consumer_secret, access_token, access_token_secret):
    '''
    Gets tweets with suicide hashtag using Twitter API

    :param consumer_token: str
    :param consumer_secret: str
    :param access_token: str
    :param access_token_secret: str
    :return: data from tweets
    '''
    auth = tweepy.OAuthHandler(hidden_keys['CONSUMER_TOKEN'], hidden_keys['CONSUMER_SECRET'])
    auth.set_access_token(hidden_keys['ACCESS_TOKEN'], hidden_keys['ACCESS_TOKEN_SECRET'])

    date_since = '2019-03-20'
    api = tweepy.API(auth)
    # '%23' is URL-encoded '#'
    data = tweepy.Cursor(api.search, q='%23suicide', since=date_since).items(50)
    return data


def forming_json(data):
    '''
    Formes a dictionary with usernames, tweets, creation dates and locations
     to work with it later on

    :param data: data from tweets
    :return: dict
    '''
    text_list = []
    text = ''
    dict_json = {'screen_names': [], 'posts': [], 'creations': [], 'locations': []} #dictionary to write into json file
    # Prints out the user screenname of who posted this
    # and a Tweet itself if data exists
    if data:
        for post in data:
            dict_json['screen_names'].append(post.user.screen_name)
            dict_json['posts'].append(post.text)
            dict_json['creations'].append(str(post.created_at))
            text += f'screen_name: {post.user.screen_name}'
            text += f'\ntext: {post.text}'

            text += f'\ncreated_at: {post.created_at}'
            # Checks if there is a Tweet's location
            # If yes, prints country and a name of this place
            # In case of missing a place of a Tweet, it prints the location of a user
            if post.place:
                dict_json['locations'].append(post.place.country + post.place.full_name)
                text += f'\ncountry: {post.place.country}'
                text += f'\nfull_name: {post.place.full_name}'
            else:
                if post.user.location:
                    dict_json['locations'].append(post.user.location)
                    text += f'\nlocation: {post.user.location}'
                else:
                    dict_json['locations'].append('No location is presented')
                    # dict_json['post {}'.format(data.index(post))]['user_location'] = 'null'
                    text += '\n' + 'location: No location is presented'
            text_list.append(text)
            text = ''

    return dict_json


def write_into_json(dict_json):
    '''
    Writes a dictionary into .json file

    :param dict_json: dict
    :return:
    '''
    with open('testing_api.json', 'w', encoding = 'utf-8') as file:
        json.dump(dict_json, file, ensure_ascii = False)


def write_into_csv(dict_json):
    '''
    Writes dictionary into .csv file

    :param dict_json: dict
    :return:
    '''
    with open('testing_api.csv', mode='w') as csv_file:

        fieldnames = ['screen_name', 'tweet_text', 'created_at',
                      'country_tweet', 'full_place_name', 'user_location']
        writer = csv.DictWriter(csv_file, fieldnames = fieldnames)
        writer.writeheader()

        for post in dict_json:
            writer.writerow(dict_json[post])


def writing_into_db(consumer_token, consumer_secret, access_token, access_token_secret):
    '''
    Creates a database using information about tweets and users who posted them

    :param consumer_token: str
    :param consumer_secret: str
    :param access_token: str
    :param access_token_secret: str
    :return:
    '''
    text = []

    while True:
        data = getting_data(consumer_token, consumer_secret, access_token, access_token_secret)
        to_write = forming_json(data)
        # writing_into_data_base(to_write)

        for i in range(len(to_write['screen_names'])):
            post = to_write['screen_names'][i] + to_write['posts'][i] + \
                                           to_write['creations'][i] + to_write['locations'][i]
            if post not in text:
                connection = sqlite3.connect('Twitter_data.db')
                cursor = connection.cursor()

                write = """INSERT INTO TWITTER (screen_name, post, created_at, location)
                        VALUES (?, ?, ?, ?)"""

                cursor.execute(write, [to_write['screen_names'][i], to_write['posts'][i],
                                       to_write['creations'][i], to_write['locations'][i]])

                connection.commit()

                connection.close()

                text.append(post)
                print('Written!')
            else:
                print('Waiting for data to reload')

        time.sleep(60)


def writing_into_txt(consumer_token, consumer_secret, access_token, access_token_secret):
    '''
    Writes dictionary into .txt file

    :param consumer_token: str
    :param consumer_secret: str
    :param access_token: str
    :param access_token_secret: str
    :return:
    '''
    text = []
    while True:

        data = getting_data(consumer_token, consumer_secret, access_token, access_token_secret)
        to_write = forming_json(data)

        for post in to_write:
            if post not in text:
                with open('testing_api.txt', 'a+') as txt_file:
                    if post not in txt_file.read():
                        txt_file.write(post + '\n' + '\n')
                text.append(post)
                print('Written!')
            else:
                print('Waiting for data to reload')

        time.sleep(60)


if __name__ == '__main__':
    hidden_keys = credentials()

    consumer_token = hidden_keys['CONSUMER_TOKEN']
    consumer_secret = hidden_keys['CONSUMER_SECRET']
    access_token = hidden_keys['ACCESS_TOKEN']
    access_token_secret = hidden_keys['ACCESS_TOKEN_SECRET']

    writing_into_db(consumer_token, consumer_secret, access_token, access_token_secret)


