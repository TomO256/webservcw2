import json
import collections
import math

## Docstring and comments created by AI, and reviewed by human

def combinedIndex(content):
    """
    Builds a combined inverted index that includes TF‑IDF scores and word positions.

    For each term, stores:
      - The documents it appears in
      - Term positions within each document (for phrase queries)
      - A TF‑IDF relevance score per document

    Args:
        content (list): List of (url, text) tuples produced by the crawler.

    Returns:
        dict: Nested inverted index structure keyed by term, then document.
    """
    index = {}
    docs = collections.defaultdict(int)  # Document frequency per term
    freq = collections.defaultdict(lambda: collections.defaultdict(int))  # Term frequency
    positions = collections.defaultdict(lambda: collections.defaultdict(list))  # Term positions

    total_docs = len(content)

    # First pass: collect frequencies and positional data
    for url, text in content:
        words = text.lower().split()
        seen = set()
        pos = 0

        for word in words:
            word = ''.join(filter(str.isalnum, word))
            if not word:
                continue

            positions[word][url].append(pos)
            freq[word][url] += 1

            if word not in seen:
                docs[word] += 1
                seen.add(word)

            pos += 1

    # Second pass: compute TF‑IDF scores
    for word in freq:
        index[word] = {}
        idf = math.log((1 + total_docs) / (1 + docs[word])) + 1

        for url in freq[word]:
            tf = freq[word][url]
            tf_weight = 1 + math.log(tf)
            score = tf_weight * idf

            index[word][url] = {
                "positions": positions[word][url],
                "score": score
            }

    return index


def rankedIndex(content):
    """
    Builds an inverted index that stores only TF‑IDF ranking scores.

    This index does not store positional information and is suitable
    for simple ranked keyword search without phrase support.

    Args:
        content (list): List of (url, text) tuples.

    Returns:
        dict: Inverted index mapping terms to documents with TF‑IDF scores.
    """
    index = {}
    docs = collections.defaultdict(int)  # Document frequency
    freq = collections.defaultdict(lambda: collections.defaultdict(int))
    total_docs = len(content)

    # Count term frequencies and document frequencies
    for url, text in content:
        words = text.lower().split()
        seen = set()

        for word in words:
            word = ''.join(filter(str.isalnum, word))
            if not word:
                continue

            freq[word][url] += 1

            if word not in seen:
                docs[word] += 1
                seen.add(word)

    # Compute TF‑IDF scores
    for word, doc in freq.items():
        index[word] = {}
        idf = math.log((1 + total_docs) / (1 + docs[word])) + 1

        for url, tf in doc.items():
            tf_weight = 1 + math.log(tf)
            index[word][url] = tf_weight * idf

    return index


def createIndex(content):
    """
    Builds a basic positional inverted index without ranking.

    Each term maps to documents containing a list of word positions,
    enabling phrase and proximity queries.

    Args:
        content (list): List of (url, text) tuples.

    Returns:
        dict: Positional inverted index.
    """
    index = {}

    for url, text in content:
        pos = 0
        words = text.lower().split(" ")

        for word in words:
            word = ''.join(filter(str.isalnum, word))
            if not word:
                continue

            if word not in index:
                index[word] = {}
            if url not in index[word]:
                index[word][url] = []

            index[word][url].append(pos)
            pos += 1

    return index


def save(index):
    """
    Serializes an index to disk as JSON.

    Args:
        index (dict): Inverted index to save.
    """
    with open("data/index.json", "w") as f:
        json.dump(index, f)


def load():
    """
    Loads a previously saved index from disk.

    Returns:
        dict: Loaded index, or False if the file does not exist.
    """
    try:
        with open("data/index.json", "r") as f:
            data = json.load(f)
            print("Load Successful")
            return data
    except FileNotFoundError:
        print(
            "Unable to find index.json. Please ensure file is named correctly, "
            "or run 'build' to create it"
        )
        return False
