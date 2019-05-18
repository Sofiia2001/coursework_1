import os
import json
import sqlite3

dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

def read_json_tweets_amount():
    '''
    Function to get amount of tweets by countries from .json file

    :return: dict
    '''
    with open(f'{dir_path}/data/tweets_amount.json') as json_file:
        data = json.load(json_file)
    return data


def get_rated_tweets_amount():
    '''
    Function sorts a list of items from dict

    :return: list
    '''
    data = read_json_tweets_amount()
    list_data = list(data.items())
    list_data.sort(key=lambda x: x[1], reverse=True)
    return list_data[1:]


def get_relevant_from_official_database():
    '''
    Function gets all needed information from database to use it in order
    to count a Spearman correlation

    :return: (list of country ratings, list of ratings by tweets data)
    '''
    sorted_data = get_rated_tweets_amount()
    with sqlite3.connect(f'{dir_path}/data/Official_data.db') as connection:
        cursor = connection.cursor()

        # insertion = "ALTER TABLE WHO ADD tweets text"
        # cursor.execute(insertion)
        # insertion = "ALTER TABLE WHO ADD tweets_rate text"
        # cursor.execute(insertion)
        # adding a new column

        country = "SELECT country FROM WHO"
        cursor.execute(country)
        countries = cursor.fetchall()
        countries_new = [country[0] for country in countries]

        for tpl_country in sorted_data:
            insertion = "UPDATE WHO SET tweets=? WHERE country=?"
            cursor.execute(insertion, [(tpl_country[1]), (tpl_country[0])])

        i = 1
        for tpl_country in sorted_data:
            if tpl_country[0] in countries_new:
                insertion_1 = "UPDATE WHO SET tweets_rate=? WHERE country=?"
                cursor.execute(insertion_1, [(str(i)), (tpl_country[0])])
                i += 1

        select = "SELECT (tweets_rate) FROM WHO WHERE tweets_rate > 0"
        cursor.execute(select)
        res = cursor.fetchall()
        res = [int(r[0]) for r in res]
        row_list = [i for i in range(1, 92)]

        return row_list, res


def count_spearman_correlation():
    '''
    Function counts a spearman correlation

    :return: float
    '''
    relevant_data = get_relevant_from_official_database()
    row_list = relevant_data[0]
    res = relevant_data[1]
    n = len(row_list)

    d_power = 0
    for i in range(len(row_list)):
        d_power += (res[i] - row_list[i]) ** 2
    spearman_correlation = round(1 - (6 * d_power) / (n * (n * n - 1)), 3)

    return spearman_correlation


# if __name__ == '__main__':
#     print(count_spearman_correlation())
    # get_relevant_from_official_database()