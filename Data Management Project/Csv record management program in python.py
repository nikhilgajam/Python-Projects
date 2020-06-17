# CSV RECORD MANAGEMENT PROGRAM IN PYTHON

import os


def add():
    print()

    rno = str(input("Enter Roll No: "))
    name = str(input("Enter Name: "))
    age = str(input("Enter Age: "))

    print()

    try:
        with open("record.csv", "r") as p:
            pass
    except FileNotFoundError:
        with open("record.csv", "a") as p:
            p.write("Roll No, Name, Age\n")

    with open("record.csv", "a") as p:
        p.write(rno + ', ' + name + ', ' + age + '\n')


def modify():
    typ = str(input("Enter Roll No To Modify: "))

    c = 0
    rno = name = age = ""
    with open("record.csv", "r") as p:
        for i in p:
            i = str(i)
            if i.startswith(typ):
                print("_________________________________________________________________\n")

                print("Existing Record\n")
                print("Roll No, Name, Age")
                print(i)
                print()
                c += 1

                print("Enter New Data")
                rno = str(input("Enter Roll No: "))
                name = str(input("Enter Name: "))
                age = str(input("Enter Age: "))
                print()
                with open("temp.csv", "a") as q:
                    q.write(rno + ", " + name + ", " + age)

            else:
                with open("temp.csv", "a") as q:
                    q.write(i)

    if c > 0:
        with open("temp.csv", "r") as q:
            data = q.read()
        with open("record.csv", "w") as p:
            p.write(data)

        print(">>>Successfully Modified<<<")

    else:
        print("Record Not There")

        os.remove("temp.csv")

    print("_________________________________________________________________\n")


def delete():
    typ = str(input("Enter Roll No To Delete: "))

    c = 0

    with open("record.csv", "r") as p:
        for i in p:
            i = str(i)
            if i.startswith(typ):
                print("_________________________________________________________________\n")

                print("Existing Record\n")
                print("Roll No, Name, Age")
                print(i)
                print()
                c += 1

            else:
                with open("temp.csv", "a") as q:
                    q.write(i)

    if c > 0:
        with open("temp.csv", "r") as q:
            data = q.read()
        with open("record.csv", "w") as p:
            p.write(data)

        print(">>>Successfully Deleted<<<")

    else:
        print("Record Not There")

    os.remove("temp.csv")

    print("_________________________________________________________________\n")


def search():
    sear = str(input("Enter Roll No To Search: "))
    c = 0

    print("_________________________________________________________________\n")

    try:
        with open("record.csv") as p:

            for i in p:
                if i.startswith(sear):
                    print("Roll No, Name, Age")
                    print(i, end="")
                    c += 1

        if c == 0:
            print("Record Not There")

    except FileNotFoundError:
        print("\nrecord.csv did not exist")

    print("_________________________________________________________________\n")


def show_all():
    print()

    try:
        with open("record.csv", "r") as p:
            data = p.read()
            if len(data) <= 20:
                print("\nNo records to display\n")
                return

        with open("record.csv", "r") as p:
            for i in p:
                print(i, end="")

    except FileNotFoundError:
        print("\nNo Files To Show (record.csv did not exist)")

    print()


# MAIN

print("Record Management Program\n")

print("1 - Add new a record")
print("2 - Modify a existing record")
print("3 - Delete a existing record")
print("4 - Search records ")
print("5 - Display all records")
print("0 - Exit the program")

while True:

    try:
        sel = int(input("Enter: "))

        if sel == 1:

            add()

        elif sel == 2:

            modify()

        elif sel == 3:

            delete()

        elif sel == 4:

            search()

        elif sel == 5:

            show_all()

        elif sel == 0:

            print("\nThanks for using")
            break

        else:

            print("\nEnter Instructed Numbers\n")

    except ValueError:
        print("\nEnter Instructed Numbers\n")
