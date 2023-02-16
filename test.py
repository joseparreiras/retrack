import sys

idx = sys.argv[1:]  # Get index of journals to get
if idx[-1] == "only":  # If only is given, get only the given journals
    idx = [int(x)-1 for x in idx[:-1]]
elif idx[-1] == "range":  # If only one journal is given, get all journals up to that rank
    if len(idx) == 2:
        idx = range(int(idx[0]))
    else:
        idx = range(int(idx[0])-1, int(idx[1]))
elif len(idx) == 0:  # If no journals are given, get all journals
    idx = range(len(journals))

print(idx)
