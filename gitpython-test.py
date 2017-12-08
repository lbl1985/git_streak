"""
Get commit history for all specified locations
INPUT:
Read in .json file with an array of specified locations
OUTPUT:
One dictionary table with all (date, #commits) pairs. Aggregated across all repos
"""
from git import Repo

def get_commit_history(path):
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

    commit_table = {}
    for commit in commits:
        date = commit.committed_datetime.strftime("%Y-%m-%d")
        if date not in commit_table:
            commit_table[date] = 1
        else:
            commit_table[date] += 1
    return commit_table
