import requests
from bs4 import BeautifulSoup
import time

## Docstring and comments created by AI, and reviewed by human

def crawl(test=False):
    """
    Entry point for the crawler.

    Crawls all quote pages and associated author pages from quotes.toscrape.com,
    returning a list of (id/url, text content) tuples suitable for indexing.

    Args:
        test (bool): If True, disables request delays for faster testing.

    Returns:
        list: Collected content from quotes and author biography pages.
    """
    url = "https://quotes.toscrape.com"
    content = []

    # Crawl quote pages first and collect author profile URLs
    content, authors = crawlQuotes(content, url, test)

    # Crawl each author page and append author biography content
    content = crawlAuthors(content, authors, test)
    return content
    
    
def crawlAuthors(content, authors, test=False):
    """
    Crawls individual author pages and extracts biography text.

    Args:
        content (list): Existing list of indexed content tuples.
        authors (set): Set of author profile URLs to crawl.
        test (bool): If True, disables request delays.

    Returns:
        list: Updated content list including author bios.
    """
    for a in authors:
        print("Indexing: " + a)
        response = requests.get(a)
        if response.status_code != 200:
            continue

        soup = BeautifulSoup(response.text, "html.parser")

        # Extract author name and biographical description
        bio = soup.find("div", class_="author-description")
        name = soup.find("h3", class_="author-title")

        if bio and name:
            final = name.text + " " + bio.text
            content.append((a, final))

        # Throttle crawl requests unless in test mode
        if not test:
            time.sleep(6)
    return content


def crawlQuotes(content, url, test=False):
    """
    Crawls paginated quote pages and extracts quotes, authors, and tags.

    Also collects links to author profile pages for secondary crawling.

    Args:
        content (list): List used to store extracted quote content.
        url (str): Base URL of the quotes website.
        test (bool): If True, disables crawl delays.

    Returns:
        tuple: (content list, set of author URLs)
    """
    authors = set()
    urlToCrawl = url

    while 1:
        print("Indexing: " + urlToCrawl)
        response = requests.get(urlToCrawl)
        if response.status_code != 200:
            break

        soup = BeautifulSoup(response.text, "html.parser")
        quotes = soup.find_all("span", class_="text")
        if not quotes:
            break

        quoteNum = 0
        for quote in quotes:
            parent = quote.find_parent("div", class_="quote")

            # Build searchable content from quote text, author name, and tags
            text = quote.text
            author = parent.find("small", class_="author").text
            tag_elements = parent.find_all("a", class_="tag")
            tags = [tag.text for tag in tag_elements]

            final = text + " " + author + " " + " ".join(tags)
            quoteNum += 1
            id = urlToCrawl + " quote:" + str(quoteNum)
            content.append((id, final))

        # Extract unique author profile links from quotes
        for quote in quotes:
            parent = quote.find_parent("div", class_="quote")
            links = parent.find_all("a", href=True)
            for link in links:
                href = link.get("href")
                if href and href.startswith("/author/"):
                    authors.add(url + href)
                    break

        # Follow pagination link if present
        try:
            next = soup.find("li", class_="next").find("a")["href"]
        except AttributeError:
            next = None

        if next:
            urlToCrawl = url + next
        else:
            print("Crawl Finished")
            break

        # Throttle crawl requests unless in test mode
        if not test:
            time.sleep(6)

    return content, authors