import requests
from bs4 import BeautifulSoup
import time


def crawl(test=False):
    url = "https://quotes.toscrape.com"
    content = []

    content, authors = crawlQuotes(content,url,test)
    content = crawlAuthors(content,authors,test)
    return content
    
    
def crawlAuthors(content,authors,test=False):
    for a in authors:
        print("Indexing: "+a)
        response = requests.get(a)
        if response.status_code !=200:
            continue
        soup = BeautifulSoup(response.text,"html.parser")
        bio = soup.find("div", class_="author-description")
        name = soup.find("h3", class_="author-title")
        if bio and name:
            final = name.text + " " + bio.text
            content.append((a, final))
        if not test:
            time.sleep(6)
    return content

def crawlQuotes(content,url,test=False):
    authors = set()
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
        quoteNum = 0
        for quote in quotes:
            parent = quote.find_parent("div", class_="quote")
            text = quote.text
            author = parent.find("small", class_="author").text
            tag_elements = parent.find_all("a", class_="tag")
            tags=[]
            for tag in tag_elements:
                tags.append(tag.text)
            final = text + " " + author + " " + " ".join(tags)
            quoteNum +=1
            id = urlToCrawl + " quote:"  + str(quoteNum)
            content.append((id, final))
        
        for quote in quotes:
            parent = quote.find_parent("div", class_="quote")

            links = parent.find_all("a", href=True)

            for link in links:
                href = link.get("href")

                if href and href.startswith("/author/"):
                    authors.add(url + href)
                    break
        try:
            next = soup.find("li",class_="next").find("a")["href"]
        except AttributeError:
            next=None
        if next:
            urlToCrawl = url + next
        else:
            print("Crawl Finished")
            break
        if not test:
            time.sleep(6)
    return content, authors