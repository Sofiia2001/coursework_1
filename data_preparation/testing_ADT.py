from .ADT_Tweets import TweetsByCountries as tbc


print('This is testing module of ADT!')
print('We will create an example of TweetsByCountries and show you its abilities!\n')

data_base = tbc('Twitter_data.db')

print('Now you can check whether you have a .json file in your folder\n')
data_base.write_into_file()

print('\nData was successfully written!\n')
print('Checking, what is amount of suicidal tweets in United States, that was counted.')
print('Remember, we limited the requests, but it always can be changed\n')
print(data_base.get_amount_in_country('United States'))

print('That is all!')