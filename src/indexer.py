import json
import collections
import math

def rankedIndex(content):
    index = {}
    docs = collections.defaultdict(int)
    freq = collections.defaultdict(lambda:collections.defaultdict(int))
    total_docs = len(content)
    for url, text in content:
        words = text.lower().split()
        seen = set()
        for word in words:
            word = ''.join(filter(str.isalnum,word))
            if not word:
                continue
            freq[word][url] +=1
            if word not in seen:
                docs[word] +=1
                seen.add(word)
    for word, doc in freq.items():
        index[word] = {}
        idf = math.log(total_docs/ (1+docs[word]))
        for url, tf in doc.items():
            tf_weight = 1 + math.log(tf)
            index[word][url] = tf_weight * idf
    return index

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