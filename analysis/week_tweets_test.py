from unittest import TestCase
from .week_tweets import WeekTweets
import unittest


class TestWeekTweets(TestCase):
    def setUp(self):
        self.my_week = WeekTweets('08.04')
        self.wrong_week = WeekTweets('31.65')
        self.ending_month_week = WeekTweets('30.01')
        
        self.week_1 = WeekTweets('22.04')
        self.week_2 = WeekTweets('01.05')

    def test_select_week(self):
        self.my_week.select_week()
        self.assertEqual(self.my_week._week_list, ['2019-04-08', '2019-04-09',
                                                   '2019-04-10', '2019-04-11',
                                                   '2019-04-12', '2019-04-13', '2019-04-14'])
        self.assertEqual(self.wrong_week.select_week(), 'This date does not exist')

    def test_select_week_from_end(self):
        self.ending_month_week.select_week()
        self.assertEqual(self.ending_month_week._week_list, ['2019-01-28', '2019-01-29', 
                                                             '2019-01-30', '2019-01-31', 
                                                             '2019-02-01', '2019-02-02', 
                                                             '2019-02-03'])

    def test_maximum_tweets_day(self):
        self.assertEqual(self.my_week.maximum_tweets_day(), 'Tuesday')
        
    def test_tweets_for_weekday(self):
        self.assertEqual(self.my_week._tweets_for_week_day()['Monday'],
                         {'general': 2261,
                          'dates':
                              {'2019-04-08', '2019-04-29', '2019-04-22', '2019-03-25'},
                          'posts': {}}) 
    
    def test_tweets_for_week(self):
        self.week_1.tweets_for_week()
        self.assertTrue(self.week_1._tweets_week_dict == {'2019-04-22': 671, '2019-04-23': 580,
                                                          '2019-04-24': 1002, '2019-04-25': 1133,
                                                          '2019-04-26': 960, '2019-04-27': 801,
                                                          '2019-04-28': 935})

        self.week_2.tweets_for_week()
        self.assertTrue(self.week_2._tweets_week_dict == {'2019-04-29': 1163, '2019-04-30': 1153,
                                                         '2019-05-01': 1106, '2019-05-02': 909, 
                                                         '2019-05-03': 1023, '2019-05-04': 117, 
                                                         '2019-05-05': 0})
        
    def test_find_week_day(self):
        self.week_1.tweets_for_week()
        self.week_2.tweets_for_week()
        self.assertEqual(self.week_1.find_week_day(), 'Thursday')
        self.assertEqual(self.week_2.find_week_day(), 'Monday')


if __name__ == '__main__':
    unittest.main()