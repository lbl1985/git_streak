
commit_history = {}

with open(r"c:\Experiment\git_streak\media_intelligence_queries_res.txt", 'r', encoding="utf-16 LE") as fp:
    lines = fp.readlines()

for line in lines:
    line = line.replace('\ufeff', '')
    date = line.split(' ')[0]    
    if date not in commit_history:
        commit_history[date] = 1
    else:
        commit_history[date] += 1

commit_history = sorted(commit_history.items(), key=lambda x:x[0])
print(commit_history)