import unittest
from vis import orgnize_data, check_fields

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

if __name__ == "__main__":
    unittest.main()