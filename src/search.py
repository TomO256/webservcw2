def display(word,index):
    if word not in index:
        print("Word not found")
        return
    print("Index position found for "+word)
    for page, pos in index[word].items():
        print("Page: "+str(page)+", Position: "+str(pos))


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