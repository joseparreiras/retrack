import json

with open('articles.json') as f:
    articles = json.load(f)


markdown = """
# 📓 Academic Journals
"""

for j, x in articles.items():
    date = x[0].get('date')
    volume = x[0].get('volume')
    issue = x[0].get('issue')
    markdown += """
---

## %s

📅 Date: %s
📕 Volume: %s
📁 Issue: %s


""" % (j, date, volume, issue)
    for article in x[0].get('articles'):
        title = article.get('title')
        author = article.get('author')
        if len(author) > 1:
            author = '; '.join(author)
        abstract = article.get('abstract')
        jel = article.get('jel')
        if len(jel) > 1:
            jel = ', '.join(jel)
        doi = article.get('doi')
        link = article.get('url')
        markdown += """
### %s
%s

#### 📄 Abstract
%s

* JEL Codes: %s
* DOI: %s

☁️ [Download here](%s)
        """ % (title, author, abstract, jel, doi, link)

with open('academic_journal.md', 'w') as f:
    f.write(markdown)
