import requests
from bs4 import BeautifulSoup
import time,json

def build():
    global index
    url = "https://quotes.toscrape.com"
    index = {}
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
        pos = 0
        for i in quotes:
            words = i.text.split(" ")
            for word in words:
                word = ''.join(filter(str.isalnum,word))
                if word not in index:
                    index[word] = {}
                if urlToCrawl not in index[word]:
                    index[word][urlToCrawl] = []
                
                index[word][urlToCrawl].append(pos)
                pos+=1
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
    with open("index.json","w") as f:
        json.dump(index,f)
    print("Sucessfully indexed webpage")
                

def load():
    global index
    try:
        with open("index.json","r") as f:
            index = json.load(f)
        print("Load Successful")
    except FileNotFoundError:
        print("Unable to find index.json. Please ensure file is named correctly, or run 'build' to create it")

def display(word):
    if word not in index:
        print("Word not found")
        return
    print("Index position found for "+word)
    for page, pos in index[word].items():
        print("Page: "+str(page)+", Position: "+str(pos))

def find(string):
    words = string.split(" ")
    results = []
    for i in words:
        if i not in index:
            print("Unable to find entry for: "+str(i))
            return
        results.append(set(index[i].keys()))
    pages = set.intersection(*results)
    if not pages:
        print("No pages located")
    else:
        print("Pages containing query")
        for i in pages:
            print(i)
    return


def run(loaded=False):
    cmd = ""
    cmd = input("Enter command\n")
    ops = cmd.split(" ",1)
    opcode = ops[0]
    if opcode =="build":
        build()
    elif opcode == "load":
        load()
        loaded = True
    elif opcode == "print":
        if not loaded:
            print("Database not loaded, please load before attempting to query")
        else:
            display(ops[1])
    elif opcode == "find":
        if not loaded:
            print("Database not loaded, please load before attempting to query")            
        else:
            find(ops[1])
    elif opcode == "exit":
        print("Exiting Gracefully")
        return
    else:
        print("""ERROR: A command should be one of the following:
build
load
print <word>
find <word>
exit""")
    run(loaded)
    


if __name__ == "__main__":
    run()