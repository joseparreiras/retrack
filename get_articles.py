import pandas as pd
from tqdm import tqdm
import json
from retrack import parse_journal

starting_url = "https://ideas.repec.org"  # Ideas URL
n_months = 1  # Number of journal versions to get
n_volumes = 3  # Number of journal versions to get

journals = pd.read_json('data/journals.json')  # Load table of journals
idx = [0, 1, 2, 3, 5, 6, 10, 11, 19, 24, 25,
       34, 221]  # Indices of journals to get
journals = journals.iloc[idx]  # Select journals

table = {}  # Initialize empty table
for i in tqdm(range(len(journals))):
    j = journals.iloc[i]  # Get journal data
    url = starting_url + j.url  # Get URL
    name = j['journal']  # Get name
    data = list(parse_journal(url, n_months, n_volumes))  # Parse journal
    if len(data)>0:
        table.update({name: data})  # Parse journal

with open('data/articles.json', 'w') as f:
    json.dump(table, f, indent=4)  # Save table
