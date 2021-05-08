import sqlite3
import time
import os

# Setting terminal title
os.system("title Compact SQL")

# Displaying text
print("\nCompact*SQLITE 3: Ver 1 Production on", time.strftime("%a %d %I:%M:%S %p"))
print('Type "exit;" to commit all the changes and exit')
print('Type "help;" to get documentation')
name = input("\ndb-name: ")

# If no name entered then default name is system
if name == "":
    name = "system"

# Creating variables of sqlite3
connect = None
cursor = None

# Connecting to database
try:
    connect = sqlite3.connect("data/"+name)
    cursor = connect.cursor()
    print("Connected.\n")

except Exception as e:
    print(e)
    exit()

# Global input string
inp_str = ""


# Operations

def get_inp():
    global inp_str
    count = 1
    inp_str = ""

    while True:
        inp_str += input("SQL " + str(count) + "> ") + " ".lower()

        if inp_str.find(";") > -1:
            inp_str = inp_str.replace(";", "").strip()
            break
        else:
            count += 1
            continue


def sql_execute(query):
    get = cursor.execute(query)
    show_status()
    get = get.fetchall()

    if str(get) != '[]':
        column_names = [description[0] for description in cursor.description]
        max_len = len(max(column_names))
        count = 0

        for i in get:
            for j in i:
                ln = len(str(j))
                if max_len < ln:
                    max_len = ln

        str_format = str("%" + str(max_len) + "s")

        for i in column_names:
            print(str_format % str(i), end=" ")
        print("\n")

        for i in get:
            for j in i:
                print(str_format % str(j), end=" ")
            print()
            count += 1

        print("\n", count, "rows selected.\n")


def show_status():
    if "insert" in inp_str:
        print("\nInserted into the table successfully.\n")
    elif "delete" in inp_str:
        print("\nDeleted from the table successfully.\n")
    elif "commit" in inp_str:
        print("\nCommitted the transaction(s) successfully.\n")
    elif "rollback" in inp_str:
        print("\nRolled back the transaction(s) successfully.\n")
    else:
        print("\nExecuted Successfully\n")


# Main loop

while True:
    get_inp()

    if inp_str == 'exit':
        print("All changes committed")
        break

    try:

        if inp_str.startswith("desc"):
            inp_str = inp_str.replace("desc ", "")
            sql_execute("PRAGMA table_info([{}])".format(inp_str))
        elif inp_str == "help":
            print("\nSQLITE 3 Documentation.\n")
            os.system("start https://www.sqlite.org/docs.html")
        else:
            sql_execute(inp_str)

    except Exception as e:
        print("\nERROR:", e, ".\n")


# Committing and closing at the end of execution
connect.commit()
connect.close()
