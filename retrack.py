import requests
from lxml import etree
from bs4 import BeautifulSoup
from datetime import datetime as dt


def parse_article(url):
    """
    Parse article from IDEAS RePEc.

    Args:
        url (str): url of the article

    Yields:
        dict: Dictionary with the following keys:
        - title: Title of the article
        - date_updated: Date the article was updated
        - author: Author of the article
        - abstract: Abstract of the article
        - jel: JEL codes of the article
        - doi: DOI of the article
        - link: Link to download the article
    """
    page = requests.get(url)  # Request page
    soup = BeautifulSoup(page.text, 'html.parser')  # Parse HTML source

    # Get metadata
    title = soup.find(
        'meta', attrs={'name': 'citation_title'}).attrs['content']
    author = soup.find(
        'meta', attrs={'name': 'citation_authors'}).attrs['content'].split(';')
    author = [x.strip() for x in author]
    abstract = soup.find(
        'meta', attrs={'name': 'citation_abstract'}).attrs['content']
    date = soup.find('meta', attrs={'name': 'date'}).attrs['content']
    jel = soup.find('meta', attrs={'name': 'jel_code'}
                    ).attrs['content'].split(';')
    if len(jel) == 1: # Format if only one JEL code
        jel = jel[0].strip()
    else:
        jel = [x.strip() for x in jel]  # Remove whitespaces
    try:  # DOI is not always available
        doi = soup.find('meta', attrs={'name': 'DOI'}).attrs['content']
    except AttributeError:
        doi = ""
    link = soup.find('input', attrs={'name': 'url'}).attrs['value']

    yield {
        'title': title,
        'date_updated': date,
        'author': author,
        'abstract': abstract,
        'jel': jel,
        'doi': doi,
        'link': link
    }


def parse_journal(url, n_months=1, n_volumes=1):
    """
    Parse journal from IDEAS RePEc.

    Args:
        url (str): Journal URL
        n_months (int): Number of months to get
        n_volumes (int): Number of volumes to get

    Yields:
        dict: Dictionary with the following keys:
        - 'date': Date of the release
        - 'volume': Volume number
        - 'issue': Issue number
        - 'articles': List of articles
    """
    from datetime import datetime as dt

    starting_url = 'https://ideas.repec.org'  # Starting URL
    # Get page
    page = requests.get(url)  # Request page
    dom = etree.HTML(page.text)  # Parse HTML source

    def parse_volume(element):
        papers = element.xpath('ul/li/b/a/@href')
        for p in papers:
            paper_url = starting_url + p
            yield from parse_article(paper_url)

    # Get data
    release = dom.xpath('//div[@id="content"]/h3/text()')  # Get release dates
    date = [x.strip().split(', ')[0] for x in release]  # Get dates
    number = [int(x.split(', ')[1].split('Volume ')[1])
              for x in release]  # Get volume numbers
    issue = [x.split(', ')[2].split('Issue ')[1]
             for x in release]  # Get issue numbers
    # Get latest volumes
    volumes = dom.xpath(
        '//h2[text()="Content"]/following-sibling::div')[:n_volumes]

    # Collect articles from the last n_months
    if n_months > 0:
        start_date = dt.today().replace(month=dt.today().month-n_months)
    else:
        start_date = dt(1900, 1, 1)  # Collect all articles if n_months <= 0
    for j, v in enumerate(volumes):
        d = date[j]  # Get date
        n = number[j]  # Get volume number
        i = issue[j]  # Get issue number
        a = []  # Initialize empty list of articles
        p_list = v.xpath('ul/li/b/a/@href')  # Get list of papers
        for p in p_list:
            paper_url = starting_url + p  # Get paper URL
            new = list(parse_article(paper_url))  # Parse paper
            # Filter by date
            new = [x for x in new if dt.strptime(
                x['date_updated'], '%Y-%m-%d') >= start_date]
            if len(new) > 0:  # Add articles to list
                a += new
            else:
                break  # Stop if no articles are found
        if len(a) > 0:
            yield {'date': d, 'volume': n, 'issue': i, 'articles': a}
