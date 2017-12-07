from git import Repo
repo = Repo("C:/Experiment/powershell/pstoolbox")
assert not repo.bare
commit_hist = list(repo.iter_commits('master'))
commits = [commit for commit in commit_hist if 'binlong' in commit.author.name.lower()]
