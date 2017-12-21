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

def orgnize_data():
    pass

def generate_html(info):
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
    html =  generate_html(info)
    # print(html)
    with open('./vis/generated.html', 'wt', encoding='utf-8') as f:
        f.write(html)

