import requests
import pandas as pd
from lxml import etree
import argparse

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('integer', metavar='N', type=int,
                    help='maximum ranking to get', default=500)
args = parser.parse_args()

# Ideas URLs
starting_url = 'https://ideas.repec.org'
url = 'https://ideas.repec.org/top/top.journals.hindex.html'
max_ranking = args.integer  # Maximum number of journals to get

# Get h-index ranking of journals
page = requests.get(url)  # Request page
dom = etree.HTML(page.text)  # Parse HTML source

# Get data
table = dom.xpath('//table')[1]  # Ranking table
rows = table.xpath('tr')[1:]  # Rows of the table

table = pd.DataFrame()  # Initialize empty table
for i, r in enumerate(rows):
    if i < max_ranking:
        journal = r.xpath('td/a')[-1]  # Journals
        publisher = journal.text.split(', ')[-1]  # Publisher
        name = journal.text[:-len(publisher)-2]
        new = pd.DataFrame({i: {
            'ranking': i+1,  # Ranking
            'journal': name,  # Name
            'publisher': publisher,  # Publisher
            'url': journal.attrib['href']  # URL
        }}).T
        table = pd.concat([table, new])  # Add new row to table

table = table[['ranking', 'journal', 'publisher', 'url']]  # Reorder columns
table.to_excel('data/journals.xlsx', index=False)  # Save table
