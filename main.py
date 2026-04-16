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
    return

def find(string):
    return


def run():
    cmd = ""
    cmd = input("Enter command\n")
    ops = cmd.split(" ",1)
    opcode = ops[0]
    if opcode =="build":
        build()
    elif opcode == "load":
        load()
    elif opcode == "print":
        display(ops[1])
    elif opcode == "find":
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
    run()
    


if __name__ == "__main__":
    run()