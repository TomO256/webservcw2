# Tom O - Web Crawler Coursework

A Python-based search engine that crawls web pages, builds an inverted index, and performs ranked retrieval using TF-IDF, with a command line interface.

## Project Structure

```
src/
├── crawler.py 
├── indexer.py   
├── search.py     

main.py           

tests/
├── test_crawler.py
├── test_indexer.py
├── test_search.py
```

## Installation

Clone the repository and install dependencies:

```
git clone https://github.com/TomO256/webservcw2.git
cd webservcw2
pip install -r requirements.txt
```

## Running the Application

Run the program:

```
python main.py
```

You will be prompted to enter commands.


## Available Commands

### Build Index

```
build
```

-  Crawls the target website
- Extracts text content
- Builds a TF-IDF index
- Saves the index to `data/index.json`


### Load Index

```
load
```

* Loads a previously saved index from disk
* Must be executed before running queries (unless `build` was just run)


### Print Word Index

```
print <word>
```
Example:

```
print friends
```

- Displays all pages containing the word
- Shows positional information (if using positional index)

---

### Search (Ranked Retrieval)

```
find <word> [additional words]
```

Examples:

```
find friends
find good friends
```

- Returns pages containing all query terms
- Results are ranked using TF-IDF
- Output is sorted by relevance score (highest first)

---

### Exit

```
exit
```

* Terminates the program

---

## Running Tests

Execute the full test suite:

```
pytest
```

This runs tests covering:

- Crawling behaviour (with mocking)
- Index construction
- TF-IDF ranking logic
- Search functionality and edge cases

# Switching Search Methods
The program is automatically setup to use the TF-IDF ranked system for returning results. The previously created find and index functions remain for completeness. These are tested within the test files, and can be switched to by changing `find_ranked` to `find` and `indexRanked` to `index` in the `main.py` file. <br>
This is not recommended.