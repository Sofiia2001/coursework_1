import sqlite3
import os


dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


def get_countries_correlation():
    with sqlite3.connect(f'{dir_path}/data/Official_data.db') as connection:
        cursor = connection.cursor()

        select_country = "SELECT country FROM WHO WHERE tweets IS NOT null"
        cursor.execute(select_country)
        res_country = cursor.fetchall()

        select_rate = "SELECT suicide_rate FROM WHO WHERE tweets IS NOT null"
        cursor.execute(select_rate)
        res_rate = cursor.fetchall()

        select_tweets = "SELECT tweets FROM WHO WHERE tweets IS NOT null"
        cursor.execute(select_tweets)
        res_tweets = cursor.fetchall()

        real_results_dict = {res_country[i][0]:
                                 round(float(res_rate[i][0].split()[0])/float(res_rate[-1][0].split()[0]), 2)
                             for i in range(len(res_country) - 1)}

        tweet_results_dict = {res_country[i][0]:
                                  round(float(res_tweets[i][0])/float(res_tweets[-1][0]), 2)
                              for i in range(len(res_country) - 1)}

        return real_results_dict, tweet_results_dict


# if __name__ == '__main__':
#     print(get_countries_correlation()[0])
#     print(get_countries_correlation()[1])