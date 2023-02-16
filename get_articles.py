from pandas import read_excel
from tqdm import tqdm
from json import dump
from retrack import parse_journal
import os
import argparse

starting_url = "https://ideas.repec.org"  # Ideas URL

# Parse arguments from command line
parser = argparse.ArgumentParser()
parser.add_argument('integer', metavar='rankings', type=int,
                    nargs='+', help='rankings to subset')
parser.add_argument('--input', '-i', help='path to excel input file',
                    type=str, default='data/journals.xlsx')
parser.add_argument('--list', '-l', action='store_true',
                    help='list journals', default=True)
parser.add_argument('--range', '-r', action='store_true',
                    help='range of journals')
parser.add_argument('--output', '-o', help='path to output file',
                    type=str, default='data/articles.json')
parser.add_argument('--n_months', '-m',
                    help='number of months to get', type=int, default=1)
parser.add_argument('--n_volumes', '-v',
                    help='number of volumes to get', type=int, default=3)
args = parser.parse_args()

# Get arguments
input_file = args.input  # Get input file
if not input_file.endswith('.xlsx'):
    # Check if input file is Excel file
    raise ValueError("Input file must be an Excel file (.xlsx)")

output_file = args.output
if not output_file.endswith('.json'):
    raise ValueError("Output file must be a JSON file (.json)")
if not os.path.exists(os.path.dirname(output_file)):
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file))

n_months = args.n_months  # Number of journal versions to get
n_volumes = args.n_volumes  # Number of journal versions to get
idx = args.integer  # Get index of journals to get
journals = read_excel(input_file)  # Load table of journals from input

# Get first n journals given by user
if args.range:  # If only one journal is given, get all journals up to that rank
    if len(idx) == 1:
        idx = range(idx[0])  # Get all journals up to given rank
    elif len(idx) == 2:
        # Get all journals between given ranks
        idx = range(idx[0]-1, idx[1])
    else:
        raise ValueError("Range only takes one or two arguments")
elif args.list:  # If only is given, get only the given journals
    idx = [int(x)-1 for x in idx]

journals = journals.iloc[idx]  # Select journals

table = {}  # Initialize empty table
for i in tqdm(range(len(journals))):
    j = journals.iloc[i]  # Get journal data
    url = starting_url + j.url  # Get URL
    name = j['journal']  # Get name
    data = list(parse_journal(url, n_months, n_volumes))  # Parse journal
    if len(data) > 0:
        table.update({name: data})  # Parse journal

with open(output_file, 'w') as f:
    dump(table, f, indent=4)  # Save table
