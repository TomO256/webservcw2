
def build():
    return

def load():
    return

def display(word):
    return

def find(string):
    return


def run():
    cmd = ""
    cmd = input("Enter command")
    ops = cmd.split(" ",1)
    opcode = ops[0]
    if opcode =="build":
        build()
    elif opcode == "load":
        load()
    elif opcode == "print":
        display(ops[1])
    elif opcode == "find":
        find(ops[1])
    else:
        print("""ERROR: A command should be one of the following:
build
load
print <word>
find <word>""")
    run()
    


if __name__ == "__main__":
    run()