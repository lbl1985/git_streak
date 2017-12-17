"""
This module will visualize the output from git_streak_ino, such as overall commits,
longest/current streak etc.
"""
import os
from jinja2 import Environment, FileSystemLoader
from git_streak_info import agg_repo_commits, last_year_table, get_commit_stats


def print_stats(stats):
    """
    print out stats
    """
    print("Overall {0} Commits, from {1} to {2}".format(stats[0][0], stats[0][1], stats[0][2]))
    print("Longest Streak {0} Days, from {1} to {2}".format(stats[1][0], \
                                                                stats[1][1], stats[1][2]))
    print("Current Streak {0} Days, from {1} to {2}".format(stats[2][0], \
                                                                stats[2][1], stats[2][2]))

def main():
    STATS = gather_data()
    print_stats(STATS)

def gather_data():
    RES_TABLE = agg_repo_commits()
    FULL_COMMIT_TABLE = last_year_table(RES_TABLE)
    STATS = get_commit_stats(FULL_COMMIT_TABLE)
    return STATS


def generate_html():
    THIS_DIR = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(THIS_DIR, 'templates')
    env = Environment(loader=FileSystemLoader(template_path),
                      trim_blocks=True)
    template = env.get_template('test_template.html')

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
        ]

    }
    print(template.render(info))

if __name__ == "__main__":
    # main()
    generate_html()
