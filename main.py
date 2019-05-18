import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import json
import os

from analysis import spearman_correlation
from analysis.countries_correlation import get_countries_correlation
from analysis.spearman_correlation import count_spearman_correlation
from analysis.week_tweets import WeekTweets


dir_path = os.path.dirname(os.path.realpath(__file__))


def data_from_json():
    '''
    Calls a function that reads .json file with information
    about number of tweets in various countries

    :return: dict
    '''
    return spearman_correlation.read_json_tweets_amount()


def get_countries():
    '''
    Reads a file with all existing countries in the world

    :return: list
    '''
    to_return = []
    with open(f'{dir_path}/data/countries.txt') as file:
        lines = file.readlines()
        for line in lines:
            line = line.split(',')
            to_return.append(line[1].strip().replace(')', '').replace("'", ''))
    return to_return


def x_and_y():
    '''
    Formes data for x asis and y asis to create a graphic

    :return: (list, list)
    '''
    data_json = data_from_json()
    countries = get_countries()
    x = []
    y = []

    for data in data_json:
        if data in countries:
            x.append(data)
            y.append(data_json[data])
    return x, y


def main_posts():
    '''
    Returns a graphic ot draw

    :return: dash html
    '''
    return html.Div(
        [
            dcc.Graph(
                id='example-graph',
                figure={
                    'data':[
                        {'x': x_and_y[0], 'y': x_and_y[1], 'type': 'bar'}
                    ],
                    'layout': {
                        'title': 'Posts by countries visualization'
                    }
                }
            )
        ]
    )


def day():
    '''
    Gets a day of a week when there were the majority of tweets posted

    :return: str
    '''
    week = WeekTweets()
    day = week.maximum_tweets_day()
    return day


def spearman():
    '''
    Calls a function from another module that counts a Spearman correlation coefficient

    :return: float
    '''
    return count_spearman_correlation()


def read_json():
    '''
    Reads .json file with daily reports about tweets in different countries

    :return: dict
    '''
    with open(f'{dir_path}/data/daily_reports.json') as file:
        data = json.load(file)
    return data


data = read_json()

x_and_y = x_and_y()

weekdays = {
    'mon': 'Monday',
    'tue': 'Tuesday',
    'wed': 'Wednesday',
    'thu': 'Thursday',
    'fri': 'Friday',
    'sat': 'Saturday',
    'sun': 'Sunday'
}

needed = get_countries_correlation()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div('Coursework research visualization', style={'color': 'black', 'fontSize': 28, 'textAlign': 'center'}),

    main_posts(),
    html.Div([
        html.Div([
               html.P(
                   dcc.Markdown('Enter the date **20.03 - 04.05** : '))
            ], style={'marginBottom': 1, 'marginTop': 1}),
        dcc.Input(
            id='date',
            type='text',
            value='20.04'
        ),

        dcc.Graph(id='week-graphic')
    ], style={'marginBottom': 100, 'marginTop': 100}),

    html.Div([
           html.Label('Choose the day of the week: '),
           dcc.Dropdown(
               id='day--week',
               options=[
                   {'label': weekdays[full], 'value': weekdays[full]}
                for full in weekdays
               ],
               value='Monday',

           ),
        dcc.Graph(id='indicator-graphic')
    ]),

    html.Div([
        dcc.Graph(id='comparison-graphic',
                  figure={'data': [
                      go.Scatter(
                          x=[i for i in needed[0]],
                          y=[needed[0][i] for i in needed[0]],
                          name='Official data correlation'
                      ),
                      go.Scatter(
                          x=[i for i in needed[1]],
                          y=[needed[1][i] for i in needed[1]],
                          name='Twitter data correlation'
                      )],
                      'layout': {
                          'title': 'Correlation'
                      }
                  })
    ], style={'marginBottom': 100, 'marginTop': 100}),

    html.Div([
        html.P(
            dcc.Markdown('Some interesting facts, that were found during the investigation:\n'
                         f' * The majority of tweets with suicide hashtag was posted on **{day()}**\n'
                         ' * The majority of tweets were posted in the ** *USA* **'), ),

        html.P(
            dcc.Markdown('The main goal of this investigation was to determine if suicidal posts'
                         ' and real suicide rates somehow depends on each other.')
        ),

        html.P(
            dcc.Markdown('So, with Spearman Correlation formula it is possible to find a coefficient of correlation.')
        ),

        html.P(
            dcc.Markdown('If this coefficient is **>** 0.5, correlation is *high*, if **<** 0.5 - *low*.')
        ),

        html.P(
            dcc.Markdown(f'Calculated Spearman correlation coefficient is **{spearman()}**')
        )
    ],
        style={'marginBottom': 250, 'marginTop': 100}),

])

@app.callback(
    Output('week-graphic', 'figure'),
    [Input('date', 'value')]
)
def update_graph(date):
    week = WeekTweets(date)
    week.tweets_for_week()
    filtered = week._tweets_week_dict

    traces = go.Scatter(
        x=[c for c in filtered],
        y=[filtered[c] for c in filtered]
    )

    return {'data': [traces],
            'layout': {'title': 'Posts in a specific week, chosen by a date'}}


@app.callback(
    Output('indicator-graphic', 'figure'),
    [Input('day--week', 'value')]
)
def update_figure(day_week_name):
    filtered = data[day_week_name]
    traces = go.Scatter(
        x=[i for i in filtered if i in get_countries()],
        y=[filtered[i] for i in filtered if i in get_countries()]
    )

    return {'data': [traces]}


server = app.server


if __name__ == '__main__':
    app.run_server(debug=False)