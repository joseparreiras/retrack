import json
import argparse
import os


parser = argparse.ArgumentParser()
parser.add_argument(
    '--output', '-o', help='path to output file', type=str, default='out/academic_journals.md'
)
parser.add_argument(
    '--input', '-i', help='path to input file', type=str, default='data/articles.json'
)
args = parser.parse_args()
input_file = args.input
if not input_file.endswith('.json'):
    raise ValueError("Input file must be a JSON file (.json)")
output_file = args.output
if not os.path.exists(os.path.dirname(output_file)):
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file))
if not output_file.endswith('.md'):
    raise ValueError("Output file must be a Markdown file (.md)")

with open(input_file) as f:
    articles = json.load(f)

head = """# 📓 Academic Journals \n
## Table of Contents:
"""

body = ""
for j, x in articles.items():
    date = x[0].get('date')
    volume = x[0].get('volume')
    issue = x[0].get('issue')
    head += """
- [%s](#%s)""" % (j, j.lower().replace(' ', '-'))
    body += """
\n
---
\n
## %s <a id = "%s"></a> \n

📅 Date: %s \n
📕 Volume: %s \n
📁 Issue: %s \n


""" % (j, j.lower().replace(' ', '-'), date, volume, issue)
    for article in x[0].get('articles'):
        title = article.get('title')
        author = article.get('author')
        if len(author) > 1:
            author = '; '.join(author)
        else:
            author = author[0]
        abstract = article.get('abstract')
        jel = article.get('jel')
        if len(jel) > 1:
            jel = ', '.join(jel)
        doi = article.get('doi')
        link = article.get('url')
        body += """
\n
### %s \n
\n 
%s
\n 
#### 📄 Abstract \n
\n 
%s \n
\n
- JEL Codes: %s \n 
- DOI: %s \n
\n
☁️ [Download here](%s) \n
""" % (title, author, abstract, jel, doi, link)

markdown = head + body
with open(output_file, 'w') as f:
    f.write(markdown)
