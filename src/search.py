## Docstring and comments created by AI, and reviewed by human

def display(word, index):
    """
    Displays all positional occurrences of a word in the inverted index.

    Prints each document containing the word along with the positions
    where the word appears. Intended for inspection and debugging.

    Args:
        word (str): The term to look up.
        index (dict): Positional inverted index structure.
    """
    if word not in index:
        print("Word not found")
        return

    print("Inverted index for " + word + ":")
    for page, data in index[word].items():
        for pos in data["positions"]:
            print(
                "Word: " + word +
                ", Page: " + str(page) +
                ", Position: " + str(pos + 1)
            )


def find(string, index):
    """
    Executes an unranked boolean AND search.

    Returns all pages that contain *every* query term, without ranking.
    Stops immediately if any term is not found in the index.

    Args:
        string (str): Space-separated query terms.
        index (dict): Inverted index.
    """
    words = string.split(" ")
    results = []

    # Collect document sets for each query term
    for i in words:
        if i not in index:
            print("Unable to find entry for: " + str(i))
            return
        results.append(set(index[i].keys()))

    # Compute intersection of all document sets
    pages = set.intersection(*results)

    if not pages:
        print("No pages located")
    else:
        print("Pages containing query")
        for i in pages:
            print(i)
    return


def find_ranked(string, index):
    """
    Executes a ranked multi-term search using TF‑IDF scores.

    Only pages containing all query terms are considered. Scores from
    individual terms are summed and results are sorted by relevance.

    Args:
        string (str): Space-separated query terms.
        index (dict): Ranked inverted index with TF‑IDF scores.

    Returns:
        list: Ranked list of (url, score) tuples.
    """
    words = string.lower().split()
    scores = {}
    pages = []

    # Gather candidate pages for each query term
    for word in words:
        if word not in index:
            print("Unable to find entry for: " + word)
            return
        pages.append(set(index[word].keys()))

    # Only keep pages containing all query terms
    pages = set.intersection(*pages)

    if not pages:
        print("No pages located")
        return []

    # Accumulate TF‑IDF scores across query terms
    for word in words:
        for url, data in index[word].items():
            if url in pages:
                scores[url] = scores.get(url, 0) + data["score"]

    # Sort results by descending relevance score
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    print("Ranked Results:")
    for url, score in ranked:
        print(url + "\t score: " + str(round(score, 3)))

    return ranked