def display(word, index):
    if word not in index:
        print("Word not found")
        return

    print("Inverted index for " + word + ":")
    for page, data in index[word].items():
        for pos in data["positions"]:
            print("Word: " + word + ", Page: " + page + ", Position: " + str(pos + 1))
            
def find(string,index):
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

def find_ranked(string, index):
    words = string.lower().split()
    scores = {}
    pages = []
    for word in words:
        if word not in index:
            print("Unable to find entry for: " + word)
            return
        pages.append(set(index[word].keys()))
    pages = set.intersection(*pages)
    if not pages:
        print("No pages located")
        return []

    for word in words:
        for url, data in index[word].items():
            if url in pages:
                scores[url] = scores.get(url, 0) + data["score"]
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    print("Ranked Results:")
    for url, score in ranked:
        print(url+"\t score: "+str(round(score, 3)))

    return ranked