Coursework research is a research of dependence of suicidal posts in Twitter and official suicide countries rates.

It is mainly directed to examine Tweets' hashtags connected to suicidal thougths, gather data based on Tweets location
or user location if the first one is not pinned. Then, creating statistics by amount of posts in various countries.
The next step is to compare official data and the one that was gathered from Twitter.

FOLDERS 

data

Twitter_data.db is database with tweets collected from Twitter with twitter_db.py module help. It has around 
18 thousand tweets with #suicide. 

Official_data.db is an official database containing information about suicides all over the world. 
daily_reports.json is a .json file, where there is some information about tweets amount in various countries depending
on the day of a week.

Cities_data.db, consists of a country, its cities and code of a country.

tweets_amount.json contains some information about a number of tweets in specific countries.

data_preparation

This folder is concentrated mainly on gathering, grouping and selecting relevant data, that is in folder data.

Official_data.db was formed with beautifulsoup_parsing.py help, where I have used Beautiful Soup library to parse
a table on a website.

ADT_Tweets.py is directed to count amount of tweets in each country. It uses both 
geonames library and created database of cities and its countries to ensure, that the information will be relevant.
Additionally, geonames has limited amount of requests and as a consequence, I had to form Cities_data.db, which 
consists of a country, its cities and code of a country. It was formed with cities_db.py module. Folder has a 
testing_ADT.py module, which actually tests an ADT.

A file testing_api.py is testing Twitter API and abilities, that can be presented by tweepy library
in working with Twitter API. Unfortunately, I cannot share a hidden module in case of private policy, that was signed
when getting Twitter API keys.

It also has functions to write gathered data into .json and .csv files.

Twitter_data.db is database with tweets collected from Twitter with twitter_db.py module help. It has around 
18 thousand tweets with #suicide. twitter_db.py module rewrites data from a .txt file with tweets, forming
a database.

analysis

week_tweets.py module is directed to analyse tweets "behaviour". It is analysing the frequency of posting tweets 
at a specific day, groups tweets by countries in a specific days, finds out in what week day there were the majority
of tweets posted. There is a week_tweets_test.py, which is a testing module for week_tweets.py, that uses unittest to 
check a program working correctly.

countries_correlation.py is a module, that counts coefficients of correlation for each country firstly depending 
on official data and then on Twitter-gathered one. It makes a simple counting like gets the last country in rates
of suicides and compares a number of suicides of each country to the last one. Then it does the same, but with the 
amount of tweets. If some kind of correlation would exist, those coefficients should have been more or less similar.

spearman_correlation.py is a module to calculate the Spearman correlation coefficient. It shows if something
depends on something else. It has a quite simple formula. The coefficient can vary from -1 to 1.
If a coefficient is > 0.5 - the correlation is high and low otherwise.


main.py is the main module that visualizes results of a research. 

