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
        "c:/Experiment/git_streak"
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
    for item in last_year_dict.items():
        date = item[0]
        if date in commit_table:
            last_year_dict[date] = commit_table[date]

    commit_history = sorted(last_year_dict.items(), key=lambda x: x[0])
    print(commit_history)


if __name__ == "__main__":
    RES_TABLE = agg_repo_commits()
    # RES_TABLE_ORDERED = sorted(RES_TABLE.items(), key=lambda x: x[0])
    # print(RES_TABLE_ORDERED)
    last_year_table(RES_TABLE)