from pandas import read_excel
from tqdm import tqdm
from json import dump
from retrack import parse_journal

starting_url = "https://ideas.repec.org"  # Ideas URL
n_months = 1  # Number of journal versions to get
n_volumes = 3  # Number of journal versions to get

journals = read_excel('data/my_journals.xlsx')  # Load table of journals

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
