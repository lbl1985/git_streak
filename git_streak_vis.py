"""
This module will visualize the output from git_streak_ino, such as overall commits,
longest/current streak etc.
"""
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

if __name__ == "__main__":
    RES_TABLE = agg_repo_commits()
    FULL_COMMIT_TABLE = last_year_table(RES_TABLE)
    STATS = get_commit_stats(FULL_COMMIT_TABLE)
    print_stats(STATS)
