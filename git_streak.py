"""
Get commit history for all specified locations
INPUT:
Read in .json file with an array of specified locations
OUTPUT:
One dictionary table with all (date, #commits) pairs. Aggregated across all repos
Author: Binlong Li      Date: 2017-12-08
"""
from datetime import datetime, timedelta
from git import Repo

def get_commit_history(path, commit_table = {}):
    """
    Get a dictionary with (date, #commits) pair for certain repo
    INPUT:
        path: eg. "C:/Experiment/powershell/pstoolbox"
    OUTPUT:
        commit_table: (date, #commits) pair
    """
    repo = Repo(path)
    assert not repo.bare
    commit_hist = list(repo.iter_commits('master'))
    commits = [commit for commit in commit_hist if 'binlong' in commit.author.name.lower()]

    for commit in commits:
        date = commit.committed_datetime.strftime("%Y-%m-%d")
        if date not in commit_table:
            commit_table[date] = 1
        else:
            commit_table[date] += 1
    return commit_table


def agg_repo_commits():
    """
    aggregate commits info a list of repos, by calling function get_commit_history
    INPUT:
        Hardcoded list of repos
    OUTPUT:
        Dictory of (date, #commits) paris
    """
    repo_list = [
        "c:/Experiment/powershell/pstoolbox",
        "c:/Experiment/git_streak",
        "C:/source/media_intelligence_queries",
        "C:/Experiment/CPP/cc150"
    ]
    res_table = {}
    for repo_path in repo_list:
        get_commit_history(repo_path, res_table)

    return res_table


def get_full_list(start_date, end_date=datetime.today()):
    """
    Dependes date range, create a full dict with (date, #commits) pairs for all
    dates within date range
    INPUT:
        start_date: start point of the date range
        end_date: ending point of the date range, default value datetime.today()
        Input could be either string or datetime object, if input as string, the format should be:
        (YYYY-MM-DD) eg. 2017-12-08
    OUTPUT:
        An empty list of (date, #commit) pairs of tuples for desired date range
    """
    if isinstance(start_date, str):
        start_date = datetime.strptime(start_date, "%Y-%m-%d")

    if isinstance(end_date, str):
        end_date = datetime.strptime(end_date, "%Y-%m-%d")

    assert isinstance(start_date, datetime)
    assert isinstance(end_date, datetime)

    delta_days = (end_date - start_date).days
    assert delta_days > 0

    tuple_list = [((end_date - timedelta(days=delta)).strftime("%Y-%m-%d"), 0) \
                    for delta in range(0, delta_days)]
    tuple_list.reverse()
    full_dict = dict(tuple_list)
    return full_dict

def last_year_table(commit_table):
    """
    Get a table with all last year dates with (date, #commits) pair
    INPUT:
        commit_table with dates, only when commits exists for that day
    OUTPUT:
        year_table, with (date, #commits) pair for last whole year
    """
    last_year_dict = get_full_list(datetime.today() + timedelta(days=-365))
    return process_full_table(last_year_dict, commit_table)


def process_full_table(full_dict, commit_table):
    """
    Feed commit_table info into full_table, and sort the full_table into time ordered
    list of tuples
    INPUT:
        full_dict: dict with all consecutive dates
        commit_table: dict with only dates, which has commits
    OUTPUT:
        full_commit_list: ordered (date, #commits) tuples, sorted by date.
    """
    for item in full_dict.items():
        date = item[0]
        if date in commit_table:
            full_dict[date] = commit_table[date]

    full_commit_list = sorted(full_dict.items(), key=lambda x: x[0])
    return full_commit_list


def get_commit_stats(full_commit_list):
    """
    Get commit stats over date period within commit_table. There are following stats:
    - Overall # of commits, date range
    - Longest streak, date range
    - Current streak, date range
    INPUT:
        full_commit_list: output from process_full_table
    OUTPUT:
        stats: list of tuples, tuple of (#commit as int, date range as str)
    """
    # full_commit_list is list of tuples in date ascend order
    stats = [(0, "", "")] * 3

    #  compute # of all commits and overall date range
    num_commits = sum([x[1] for x in full_commit_list])
    stats[0] = (num_commits, full_commit_list[0][0], full_commit_list[-1][0])

    # revert the list, to make today as the first
    full_commit_list.reverse()

    longest_streak = 0
    current_streak = 0
    last_day_has_commit = False
    # in case, most recent date does not have any commit
    # use this setting to verify current streak computation
    current_streak_start = full_commit_list[0][1]
    current_streak_end = full_commit_list[0][1]

    for day in full_commit_list:
        if day[1] > 0:
            # when there is commit
            if not last_day_has_commit:
                # new streak starts
                current_streak = 1
                current_streak_end = day[0]
                current_streak_start = day[0]
            else:
                # streak continues
                current_streak += 1
                current_streak_start = day[0]
            last_day_has_commit = True
        else:
            # when there is no commit
            if last_day_has_commit:
                # One finishedneed, need clean up processing
                # NOTE: Two consecutive days without commit nothing need to be changed
                # Special case for current streak processing first
                if current_streak_end == full_commit_list[0][0]:
                    stats[2] = (current_streak, current_streak_start, current_streak_end)
                if current_streak > longest_streak:
                    # current streak is the longest streak we have seen so far
                    longest_streak = current_streak
                    stats[1] = (current_streak, current_streak_start, current_streak_end)

                # reset temporal variables
                current_streak = 0
                current_streak_start = ""
                current_streak_end = ""
                last_day_has_commit = False

    return stats


def print_stats(stats):
    """
    print out stats
    """
    print("Overall {0} Commits, from {1} to {2}".format(stats[0][0], stats[0][1], stats[0][2]))
    print("Longest Streak {0} Days, from {1} to {2}".format(stats[1][0], \
                                                                stats[1][1], stats[1][2]))
    print("Current Streak {0} Days, from {1} to {2}".format(stats[2][0], \
                                                                stats[2][1], stats[2][2]))


if __name__ == "__main__":
    RES_TABLE = agg_repo_commits()
    FULL_COMMIT_TABLE = last_year_table(RES_TABLE)
    STATS = get_commit_stats(FULL_COMMIT_TABLE)
    print_stats(STATS)
