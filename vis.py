"""
This module will visualize the output from info, such as overall commits,
longest/current streak etc.
"""
import os
from jinja2 import Environment, FileSystemLoader
from info import agg_repo_commits, last_year_table, get_commit_stats


def print_stats(stats):
    """
    print out stats
    """
    print("Overall        {0:>5} Commits \t\t{1} - {2}".format(stats[0][0], stats[0][1], stats[0][2]))
    print("Longest Streak {0:>5} Days \t\t{1} - {2}".format(stats[1][0], \
                                                                stats[1][1], stats[1][2]))
    if stats[2][0] > 0:
        print("Current Streak {0:>5} Days \t\t{1} - {2}".format(stats[2][0], \
                                                                stats[2][1], stats[2][2]))
    else:
        print("Current Streak {0:>5} Day \t\tNo commit today".format(0))

def main():
    STATS = gather_data()
    print_stats(STATS)

def gather_data():
    RES_TABLE = agg_repo_commits()
    FULL_COMMIT_TABLE = last_year_table(RES_TABLE)
    STATS = get_commit_stats(FULL_COMMIT_TABLE)
    return STATS

def orgnize_data(STATS):
    pass

def check_fields(var, field, t):
    """
    utility function to check whehter certain field exists in var
    """    
    if field not in var:
        raise(ValueError("field {0} is not in dict".format(field)))
    if type(var[field]) is not t:
        raise(TypeError("field {0} should be type {1}".format(field, t)))


def verify_info(info):
    """Verify info as a assistant function to generate_html"""
    check_fields(info, 'months', list)
    check_fields(info, 'offsets', list)
    check_fields(info, 'days', list)
    if len(info['days']) == 0:
        raise ValueError('info[days] contains 0 days data')
    check_fields(info['days'][0], 'date', str)
    check_fields(info['days'][0], 'commits', int)
    check_fields(info['days'][0], 'activity', int)
    
    check_fields(info, 'overall', dict)
    check_fields(info['overall'], 'commits', int)
    check_fields(info['overall'], 'start_date', str)
    check_fields(info['overall'], 'end_date', str)

    check_fields(info, 'longest_streak', dict)
    check_fields(info['longest_streak'], 'days', int)
    check_fields(info['longest_streak'], 'start_date', str)
    check_fields(info['longest_streak'], 'end_date', str)

    check_fields(info, 'current_streak', dict)
    check_fields(info['current_streak'], 'days', int)
    check_fields(info['current_streak'], 'start_date', str)
    check_fields(info['current_streak'], 'end_date', str)

def generate_html(info):
    """
    apply info from input variable info onto template.html by using jinga2, 
    eventually will generate a string for the html
    At first generate html will in charge of checking the data strcture and 
    fiedls on info
    """
    verify_info(info)
    THIS_DIR = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(THIS_DIR, 'templates')
    env = Environment(loader=FileSystemLoader(template_path),
                      trim_blocks=True)
    template = env.get_template('test_template.html')
    html = template.render(info)
    return html

if __name__ == "__main__":
    # main()
    info = {
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
            "days": 2,
            "start_date": "2017-02-03",
            "end_date": "2017-05-03"
        },
        "current_streak": {
            "days": 3,
            "start_date": "2017-12-18",
            "end_date": "2017-12-20"
        }        
    }
    html =  generate_html(info)
    # print(html)
    with open('./vis/generated.html', 'wt', encoding='utf-8') as f:
        f.write(html)

