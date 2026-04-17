from crawler import crawl
from indexer import load, save, createIndex
from search import find, display

def run(index=False):
    cmd = ""
    cmd = input("Enter command\n").lower()
    ops = cmd.split(" ",1)
    opcode = ops[0]
    if opcode =="build":
        pages = crawl()
        index = createIndex(pages)
        save(index)
    elif opcode == "load":
        index = load()
    elif opcode == "print":
        if not index:
            print("Database not loaded, please load before attempting to query")
        else:
            display(ops[1],index)
    elif opcode == "find":
        if not index:
            print("Database not loaded, please load before attempting to query")            
        else:
            find(ops[1],index)
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