from pandas import read_excel
from tqdm import tqdm
from json import dump
from retrack import parse_journal
import sys

starting_url = "https://ideas.repec.org"  # Ideas URL
n_months = 1  # Number of journal versions to get
n_volumes = 3  # Number of journal versions to get

journals = read_excel(sys.argv[1])  # Load table of journals from input
# Get first n journals given by user
idx = sys.argv[2:]  # Get index of journals to get
if idx[-1] == "only":  # If only is given, get only the given journals
    idx = [int(x)-1 for x in idx[:-1]]
elif idx[-1] == "range":  # If only one journal is given, get all journals up to that rank
    if len(idx) == 2:
        idx = range(int(idx[0]))
    else:
        idx = range(int(idx[0])-1, int(idx[1]))
elif len(idx) == 0:  # If no journals are given, get all journals
    idx = range(len(journals))

journals = journals.iloc[idx]  # Select journals

table = {}  # Initialize empty table
for i in tqdm(range(len(journals))):
    j = journals.iloc[i]  # Get journal data
    url = starting_url + j.url  # Get URL
    name = j['journal']  # Get name
    data = list(parse_journal(url, n_months, n_volumes))  # Parse journal
    if len(data) > 0:
        table.update({name: data})  # Parse journal

with open('data/articles.json', 'w') as f:
    dump(table, f, indent=4)  # Save table
