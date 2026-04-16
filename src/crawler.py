import requests
from bs4 import BeautifulSoup
import time

def crawl():
    url = "https://quotes.toscrape.com"
    content = []
    urlToCrawl = url
    while 1:
        print("Indexing: "+urlToCrawl)
        response = requests.get(urlToCrawl)
        if response.status_code !=200:
            break
        soup = BeautifulSoup(response.text, "html.parser")
        quotes = soup.find_all("span",class_="text")
        if not quotes:
            break
        content.append((urlToCrawl,quotes))
        try:
            next = soup.find("li",class_="next").find("a")["href"]
        except AttributeError:
            next=None
        if next:
            urlToCrawl = url + next
        else:
            print("Crawl Finished")
            break
        
        time.sleep(6)
    return content