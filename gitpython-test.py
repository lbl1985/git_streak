"""
Get commit history for all specified locations
INPUT:
Read in .json file with an array of specified locations
OUTPUT:
One dictionary table with all (date, #commits) pairs. Aggregated across all repos
"""
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


if __name__ == "__main__":
    RES_TABLE = agg_repo_commits()
    RES_TABLE_ORDERED = sorted(RES_TABLE.items(), key=lambda x: x[0])
    print(RES_TABLE_ORDERED)
