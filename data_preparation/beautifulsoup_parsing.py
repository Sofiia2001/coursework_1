import requests
from bs4 import BeautifulSoup
import sqlite3


def get_html(url):
    '''
    Gets html code of a web page

    :param url: link to a web page
    :return: html text
    '''
    to_refactor = requests.get(url)

    return to_refactor.text


def get_countries(html):
    '''
    Gets countries names from html code of a web page

    :param html: str html code
    :return: dict
    '''
    soup = BeautifulSoup(html, 'html.parser')
    td_tags = soup.find('table', class_='table-striped').find_all('td')

    suicide_rates = [td.string for td in td_tags if td.string is not None]

    country_deaths_dict = {suicide_rates[i]: suicide_rates[i+1] for i in range(0, len(suicide_rates), 3)}
    return country_deaths_dict


def write_into_database(data):
    '''
    Writes parsed table from a web page into a database

    :param data: dict
    :return:
    '''
    connection = sqlite3.connect('Official_data.db')
    cursor = connection.cursor()

    # cursor.execute("""CREATE TABLE WHO (
    #                     country text,
    #                     suicide_rate text
    #                     )""")
    #
    # connection.commit()

    for ind, tpl_info in enumerate(data.items()):
        write = "INSERT INTO WHO (country, suicide_rate) VALUES (?, ?)"
        cursor.execute(write, [(tpl_info[0]), (tpl_info[1])])

    connection.commit()

    connection.close()


if __name__ == '__main__':
    url = 'http://worldpopulationreview.com/countries/suicide-rate-by-country/'
    info = get_countries(get_html(url))
    write_into_database(info)
