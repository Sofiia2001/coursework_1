import sqlite3


def writing_into_data_base(data):
    connection = sqlite3.connect('Twitter_data.db')
    cursor = connection.cursor()

    cursor.execute("""CREATE TABLE TWITTER (
                        screen_name text,
                        post text,
                        created_at text,
                        location text
                        )""")

    connection.commit()

    for i in range(len(data['screen_names'])):
        write = """INSERT INTO TWITTER (screen_name, post, created_at, location)
                VALUES (?, ?, ?, ?)"""

        cursor.execute(write, [data['screen_names'][i], data['posts'][i],
                               data['creations'][i], data['locations'][i]])

    connection.commit()

    connection.close()


def reading_from_file():
    with open('testing_api.txt') as tw_api:
        lines = tw_api.readlines()
        dct = {'screen_names': [], 'posts': [], 'creations': [], 'locations': []}
        for line in lines:
            if line.startswith('screen_name'):
                screen_name = line[line.index(':'):]
                dct['screen_names'].append(screen_name)

            elif line.startswith('text'):
                post = line[line.index(':'):]
                dct['posts'].append(post)

            elif line.startswith('created_at'):
                created_at = line[line.index(':'):]
                dct['creations'].append(created_at)

            elif line.startswith('location'):
                location = line[line.index(':'):]
                dct['locations'].append(location)

            elif line.startswith('country'):
                ind = lines.index(line)
                location = line[line.index(':'):]
                line_2 = lines[ind + 1]
                if line_2.startswith('full_name'):
                    location += line_2[line_2.index(':'):]
                dct['locations'].append(location)

    return dct

if __name__ == '__main__':
    data = reading_from_file()
    writing_into_data_base(data)






