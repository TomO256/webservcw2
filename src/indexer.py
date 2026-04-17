import json

def createIndex(content):
    index = {}
    for url, text in content:
        pos = 0
        words = text.lower().split(" ")
        for word in words:
            word = ''.join(filter(str.isalnum,word))
            if not word:
                continue
            if word not in index:
                index[word] = {}
            if url not in index[word]:
                index[word][url] = []
            index[word][url].append(pos)
            pos+=1
    return index

def save(index):
    with open("data/index.json","w") as f:
        json.dump(index,f)

def load():
    try:
        with open("data/index.json","r") as f:
            data = json.load(f)
            print("Load Successful")
            return data
    except FileNotFoundError:
        print("Unable to find index.json. Please ensure file is named correctly, or run 'build' to create it")
        return False