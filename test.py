import unittest
from vis import orgnize_data, check_fields, get_monthList, get_activity

class VisTests(unittest.TestCase):
    """ Test for functions involved in organization stage """
    def setUp(self):
        """ create test data """
        self._stats = [            
        ]
        self._info = {
            'title': 'hello world 2',
            'months': ['DEC', 'JAN', 'FEB'],
            'offsets': ['', ''],
            'days': [
                {
                    "date": '2016-12-14',
                    "commits": 5,
                    "activity": 3
                },
                {
                    'date': '2016-12-15',
                    'commits': 4,
                    "activity": 2
                }
            ],
            'overall': {
                "commits": 20,
                "start_date": "2016-12-20",
                "end_date": "2017-12-21"
            },
            "longest_streak": {
                "days": "3",
                "start_date": "2017-02-03",
                "end_date": "2017-05-03"
            },
            "current_streak": {
                "days": "3",
                "start_date": "2017-12-18",
                "end_date": "2017-12-20"
            }        
        }


    def tearDown(self):
        """tear down info"""
        pass

    
    def test_check_fields(self):
        """
        test on function check_fields 
        """
        info = {'months':'test_month', 
            'days': [
                {
                    "overall": 23,
                    "longest": "test"
                }
            ]
        }
        self.assertRaises(ValueError, check_fields, info, 'month', list)
        self.assertRaises(TypeError, check_fields, info, 'months', list)
        self.assertRaises(ValueError, check_fields, info['days'][0], 'fail', int)


    def test_get_monthList(self):
        """
        test on function get_monthList
        """
        self.assertRaises(ValueError, get_monthList, "2017-29_20")
        self.assertListEqual(
            get_monthList('2016-12-23')
            ,['DEC', 'JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG'
            , 'SEP', 'OCT', 'NOV', 'DEC' ] )

    
    def test_get_activity(self):
        """ test on function get_activity """
        q = [1, 15, 20, 30, 40]
        self.assertEqual(get_activity(0, q), 0)
        self.assertEqual(get_activity(1, q), 1)
        self.assertEqual(get_activity(13, q), 1)
        self.assertEqual(get_activity(15, q), 2)
        self.assertEqual(get_activity(16, q), 2)
        self.assertEqual(get_activity(19, q), 2)
        self.assertEqual(get_activity(20, q), 3)
        self.assertEqual(get_activity(25, q), 3)
        self.assertEqual(get_activity(29, q), 3)
        self.assertEqual(get_activity(30, q), 4)
        self.assertEqual(get_activity(35, q), 4)
        self.assertEqual(get_activity(39, q), 4)
        self.assertEqual(get_activity(40, q), 4)

if __name__ == "__main__":
    unittest.main()