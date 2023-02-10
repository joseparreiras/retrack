import pandas as pd
from tqdm import tqdm
import json
from retrack import parse_journal

starting_url = "https://ideas.repec.org"  # Ideas URL
number = 1  # Number of journal versions to get

journals = pd.read_json('journals.json')  # Load table of journals
idx = [0, 1, 2, 3, 5, 6, 10, 11, 19, 24, 25,
       34, 221]  # Indices of journals to get
journals = journals.iloc[idx]  # Select journals

table = {}  # Initialize empty table
for i in tqdm(range(len(journals))):
    j = journals.iloc[i]  # Get journal data
    url = starting_url + j.url  # Get URL
    name = j['journal']  # Get name
    table.update({name: list(parse_journal(url, number))})  # Parse journal

with open('articles.json', 'w') as f:
    json.dump(table, f, indent=4)  # Save table
