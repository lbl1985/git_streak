"""
This module will visualize the output from info, such as overall commits,
longest/current streak etc.
"""
import os, math
from datetime import datetime
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
    (STATS, FULL_COMMIT_TABLE, DATA_STRUCTURE) = gather_data()
    print_stats(STATS)
    html = generate_html(DATA_STRUCTURE)
    with open('./vis/generated.html', 'wt', encoding='utf-8') as f:
        f.write(html)


def html_main():
    """ main function for generating html. """
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

def gather_data():
    RES_TABLE = agg_repo_commits()
    FULL_COMMIT_TABLE = last_year_table(RES_TABLE)
    STATS = get_commit_stats(FULL_COMMIT_TABLE)
    DATA_STRUCTURE = orgnize_data(FULL_COMMIT_TABLE, STATS)
    return (STATS, FULL_COMMIT_TABLE, DATA_STRUCTURE)


def get_monthList(start_date):
    """
    based on start_date to get a list of 13 months
    INPUT: 
        start_date: string in format of %Y-%m-%d
    OUTPUT:
        months: list of strings for months
    """
    try:
        d = datetime.strptime(start_date, '%Y-%m-%d')
    except ValueError as e:
        raise(ValueError(
            '{0} and should both be in format of %Y-%m-%d'
            .format(start_date)))

    months = []
    for i in range(0, 13):
        m = (d.month + i) % 12
        if m == 0:
            m = 12
        months.append(datetime(d.year, m, 1).strftime('%b').upper())
    return months


def get_activity(v, q):
    """
    get value is between in which area according to q
    """
    if v == 0:
        return 0
    if v == q[0]:
        return 1
    if v == q[-1]:
        return len(q) - 1

    for id, item in enumerate(q):
        if (id < len(q) - 1):
            if v >= item and v < q[id + 1]:
                return id + 1

def get_days(table):
    """
    from table, compute a list of dict, which including 3 fields:
        date: as name
        commits: # of commits for that day
        activity: level of active, from 1 to 4
    INPUT:
        table: list of tuples, (datestr, #commits)
    OUTPUT:
        days: list of dictionaries, with above mentioned strucuture 
    """
    non_zero = [t[1] for t in table if t[1] != 0]
    q0 = min(non_zero)
    q4 = max(non_zero)
    q1 = math.floor( (3 * q0 + q4) / 4)
    q2 = math.floor( (q0 + q4) / 2)
    q3 = math.floor( (q0 * 3 * q4) / 4)
    q = [q0, q1, q2, q3, q4]
    
    days = []
    # reversed_table = list(reversed(table))
    for t in table:
        d = {
            'date': t[0],
            'commits': t[1],
            'activity': get_activity(t[1], q)
        }
        days.append(d)

    return days
        

def orgnize_data(FULL_COMMIT_TABLE, STATS):
    """
    Combine FULL_COMMIT_TABLE and STATS into one dictionary, which applies with 
    function verify_info, or check example in html_main()
    """
    start_date = FULL_COMMIT_TABLE[0][0]
    start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')

    months = get_monthList(start_date)
    offsets = [''] * (6 - start_date_obj.weekday())
    d = {
        'months': months,
        'offsets': offsets,
        'days': get_days(FULL_COMMIT_TABLE),
        'overall': {
            'commits': STATS[0][0],
            'start_date': STATS[0][1],
            'end_date': STATS[0][2]
        },
        'longest_streak': {
            'days': STATS[1][0],
            'start_date': STATS[1][1],
            'end_date': STATS[1][2]
        },
        'current_streak': {
            'days': STATS[2][0],
            'start_date': STATS[2][1],
            'end_date': STATS[2][2]
        }
    }
    return d

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
    main()
    
