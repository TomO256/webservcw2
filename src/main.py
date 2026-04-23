from crawler import crawl
from indexer import load, save, createIndex, rankedIndex,combinedIndex
from search import find, display, find_ranked

def run(index=False):
    cmd = ""
    cmd = input("Enter command\n").lower()
    ops = cmd.split(" ",1)
    opcode = ops[0]
    if opcode =="build":
        pages = crawl(True)
        #index = createIndex(pages)
        index = combinedIndex(pages)
        save(index)
    elif opcode == "load":
        index = load()
    elif opcode == "print":
        if not index:
            print("Database not loaded, please load before attempting to query")
        else:
            if len(ops) !=2:
                print("Usage: print <word>")
            else:
                display(ops[1],index)
            
    elif opcode == "find":
        if not index:
            print("Database not loaded, please load before attempting to query")            
        else:
            try:
                # find(ops[1],index)
                find_ranked(ops[1],index)
            except IndexError:
                print("Usage: find <word> [additional words]")
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
    run(index)
    


if __name__ == "__main__":
    run()