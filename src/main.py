from crawler import crawl
from indexer import load, save, createIndex, rankedIndex, combinedIndex
from search import find, display, find_ranked

## Docstring and comments created by AI, and reviewed by human

def run(index=False):
    """
    Command-line interface loop for the search engine.

    Supports building the index, loading a saved index, printing index
    entries for a term, executing ranked searches, and exiting the program.

    Args:
        index (dict or False): The currently loaded search index.
    """
    cmd = ""
    cmd = input("Enter command\n").lower()
    ops = cmd.split(" ", 1)
    opcode = ops[0]

    if opcode == "build":
        # Crawl the website and build a combined (positional + ranked) index
        pages = crawl(True)
        index = combinedIndex(pages)
        save(index)

    elif opcode == "load":
        # Load a previously saved index from disk
        index = load()

    elif opcode == "print":
        # Display raw index entries for a given word
        if not index:
            print("Database not loaded, please load before attempting to query")
        else:
            if len(ops) != 2:
                print("Usage: print <word>")
            else:
                display(ops[1], index)

    elif opcode == "find":
        # Execute a ranked search query
        if not index:
            print("Database not loaded, please load before attempting to query")
        else:
            try:
                find_ranked(ops[1], index)
            except IndexError:
                print("Usage: find <word> [additional words]")

    elif opcode == "exit":
        # Terminate the program
        print("Exiting Gracefully")
        return

    else:
        # Handle invalid commands
        print("""ERROR: A command should be one of the following:
build
load
print <word>
find <word>
exit""")

    # Recursively prompt for the next command
    run(index)


if __name__ == "__main__":
    run()