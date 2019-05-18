import sqlite3


def write_into_country_db():
    '''
    Creates data base containing countries and their cities
    :return:
    '''
    connection = sqlite3.connect('Cities_data.db')
    cursor = connection.cursor()

    cursor.execute("""CREATE TABLE CITIES (
                        city text,
                        country_name text,
                        cc_fips text
                     )""")

    connection.commit()

    with open('GEODATASOURCE-CITIES-FREE.TXT/GEODATASOURCE-CITIES-FREE.TXT') as country_file:
        text = country_file.readlines()
        for ind in range(1, len(text)):
            line = text[ind].split('\t')

            write = """INSERT INTO CITIES (city, cc_fips) VALUES (?, ?)"""
            cursor.execute(write, [(line[1].replace('\n', '')), (line[0].replace('\n', ''))])

        connection.commit()

    with open('GEODATASOURCE-CITIES-FREE.TXT/GEODATASOURCE-COUNTRY.TXT') as country_file:
        text = country_file.readlines()
        for ind in range(1, len(text)):
            line = text[ind].split('\t')

            write = """UPDATE CITIES SET country_name=? WHERE cc_fips=?"""

            cursor.execute(write, [(line[3].replace('\n', '')), (line[0].replace('\n', ''))])

        connection.commit()
    connection.close()

# write_into_country_db()

