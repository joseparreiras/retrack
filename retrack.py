import requests
from lxml import etree


def parse_article(url):
    """
    Parse article from IDEAS RePEc.

    Args:
        url (str): url of the article

    Yields:
        dict: Dictionary with the following keys:
        - title: Title of the article
        - author: Author of the article
        - abstract: Abstract of the article
        - jel: JEL codes of the article
        - doi: DOI of the article
        - link: Link to download the article
    """
    # Get page
    page = requests.get(url)  # Request page
    dom = etree.HTML(page.text)  # Parse HTML source

    # Get data
    title = dom.xpath('//div[@id="title"]/h1/text()').pop()  # Get title
    title = title.lstrip('[“').rstrip('\,”]')  # Clean title
    author = dom.xpath('//*[@class="authorname"]/text()')  # Get author
    abstract = dom.xpath(
        '//*[@id="abstract-body"]/text()').pop()  # Get abstract
    jel = dom.xpath('//a[contains(@href,"/j/")]/@href')  # Get JEL codes
    # Clean JEL codes (remove /j/ and .html)
    jel = [j[3:].split('.html')[0] for j in jel if len(j) > 3]
    doi = dom.xpath(
        '//div[@id="biblio-body"]/text()')[-1].split('DOI: ')[-1]  # Get DOI
    link = dom.xpath('//*[@id="download"]/form/input/@value')[1]

    yield {
        'title': title,
        'author': author,
        'abstract': abstract,
        'jel': jel,
        'doi': doi,
        'link': link
    }


def parse_journal(url, number=1):
    """
    Parse journal from IDEAS RePEc.

    Args:
        url (str): Journal URL
        number (int): Number of volumes to get

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
    release = dom.xpath('//div[@id="content"]/h3/text()')
    date = [x.strip().split(', ')[0] for x in release]
    number = [int(x.split(', ')[1].split('Volume ')[1]) for x in release]
    issue = [x.split(', ')[2].split('Issue ')[1] for x in release]
    volumes = dom.xpath('//h2[text()="Content"]/following-sibling::div')[:-1]

    for j, v in enumerate(volumes[:number]):
        d = date[j]
        n = number[j]
        i = issue[j]
        yield {'date': d, 'volume': n, 'issue': i, 'articles': list(parse_volume(v))}
