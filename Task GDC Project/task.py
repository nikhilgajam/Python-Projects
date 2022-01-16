import sys
import os

// Use command line arguments to make this code work

pending = []
completed = []
pending_c = completed_c = 0


def helps():
    print('''Usage :-
$ ./task add 2 hello world    # Add a new item with priority 2 and text "hello world" to the list
$ ./task ls                   # Show incomplete priority list items sorted by priority in ascending order
$ ./task del INDEX            # Delete the incomplete item with the given index
$ ./task done INDEX           # Mark the incomplete item with the given index as complete
$ ./task help                 # Show usage
$ ./task report               # Statistics''')


def create_task():
    p = open("task.txt", "w")
    p.close()


def create_completed():
    p = open("completed.txt", "w")
    p.close()


def ls():
    for k, i in enumerate(pending):
        num_index = i.find(" ")
        print(str(k+1) + ". " + i[num_index+1:].replace("\n", "") + " [" + i[0:num_index] + "]")


def add(var1, var2):
    pending.append(var1 + " " + var2)
    print('Added task: "' + var2 + '" with priority ' + var1)


def delete(index):
    try:
        pending.pop(int(index)-1)
        print("Deleted item with index " + index)
    except Exception:
        print("Error: item with index " + index + " does not exist. Nothing deleted.")


def done(index):
    try:
        x = pending.pop(int(index)-1)
        temp = x.find(" ")
        completed.append(x[temp+1:])
        print("Deleted item with index " + index)
    except Exception:
        print("Error: no incomplete item with index " + index + " exists.")


def get_report():
    print("Pending : \n" + str(pending_c), end="")
    for k, i in enumerate(pending):
        num_index = i.find(" ")
        print(str(k+1) + ". " + i[num_index+1:].replace("\n", "") + " [" + i[0:num_index] + "]")
    print()
    print("Completed : " + str(completed_c), end="\n")
    for k, i in enumerate(completed):
        num_index = i.find(" ")
        print(str(k+1) + ". " + i)


def start():
    global completed_c, pending_c
    p = open("task.txt", "r")
    for i in p:
        pending.append(i.replace("\n", ""))
        pending_c += 1
    p.close()
    p = open("completed.txt", "r")
    for i in p:
        completed.append(i.replace("\n", ""))
        completed_c += 1
    p.close()


def end():
    p = open("task.txt", "w")
    pending.sort()
    for i in pending:
        p.write(i + "\n")
    p.close()
    p = open("completed.txt", "w")
    for i in completed:
        p.write(i + "\n")
    p.close()


if __name__ == "__main__":
    
    if not os.path.isfile("task.txt"):
        create_task()

    if not os.path.isfile("completed.txt"):
        create_completed()

    start()

    if len(sys.argv) == 1 or sys.argv[1] == "help":
        helps()
    elif sys.argv[1] == "report":
        get_report()
    elif sys.argv[1] == "ls":
        ls()
    elif sys.argv[1] == "add":
        try:
            add(sys.argv[2], sys.argv[3])
        except Exception:
            print("Error: Missing tasks string. Nothing added!")
    elif sys.argv[1] == "del":
        try:
            delete(sys.argv[2])
        except Exception:
            print("Error: Missing NUMBER for deleting tasks.")
    elif sys.argv[1] == "done":
        try:
            done(sys.argv[2])
        except Exception:
            print("Error: Missing NUMBER for marking tasks as done.")

    end()
