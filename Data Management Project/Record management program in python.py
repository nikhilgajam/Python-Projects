# RECORD MANAGEMENT PROGRAM IN PYTHON

import os


def add():
    print()

    rno = str(input("Enter Roll No: "))
    name = str(input("Enter Name: "))
    age = str(input("Enter Age: "))

    print()

    with open("record.txt", "a") as p:
        p.write(rno + '_' + name + '_' + age + ',')


def modify():
    typ = str(input("Enter Roll No To Modify: "))
    with open("record.txt", "r") as p:
        data = p.read()
        data = data.split(',')

    c = 0

    with open("temp.txt", "w") as q:
        for i in data:
            doc = i.split('_')
            try:
                rno = doc[0]
                name = doc[1]
                age = doc[2]

                if typ == rno:

                    print("_________________________________________________________________\n")

                    print("Existing Record\n")
                    print('Roll No:', rno)
                    print('Name:', name)
                    print('Age:', age)
                    print()
                    c += 1

                    print("Enter New Data")
                    rno = str(input("Enter Roll No: "))
                    name = str(input("Enter Name: "))
                    age = str(input("Enter Age: "))
                    print()

                    q.write(rno + '_' + name + '_' + age + ',')
                else:

                    q.write(rno + '_' + name + '_' + age + ',')

            except IndexError:
                pass

    if c > 0:
        with open("temp.txt", "r") as q:
            data = q.read()
        with open("record.txt", "w") as p:
            p.write(data)

        os.remove("temp.txt")
        print(">>>Successfully Modified<<<")

    else:
        print("Record Not There")

    print("_________________________________________________________________\n")


def delete():
    typ = str(input("Enter Roll No To Delete: "))
    with open("record.txt", "r") as p:
        data = p.read()
        data = data.split(',')

    c = 0

    with open("temp.txt", "w") as q:
        for i in data:
            doc = i.split('_')
            try:
                rno = doc[0]
                name = doc[1]
                age = doc[2]

                if typ == rno:
                    print("_________________________________________________________________\n")

                    print("Existing Record\n")
                    print('Roll No:', rno)
                    print('Name:', name)
                    print('Age:', age)
                    print()
                    c += 1

                else:

                    q.write(rno + '_' + name + '_' + age + ',')

            except IndexError:
                pass

    if c > 0:
        with open("temp.txt", "r") as q:
            data = q.read()
        with open("record.txt", "w") as p:
            p.write(data)

        os.remove("temp.txt")
        print(">>>Successfully Deleted<<<")

    else:
        print("Record Not There")

    print("_________________________________________________________________\n")


def search():
    data = sear = ""

    try:
        with open("record.txt", "r") as p:
            data = p.read()
        data = data.split(',')

        sear = str(input("Enter Roll No: "))

    except FileNotFoundError:
        print("\nRecord.txt did not exist")

    c = 0

    print("_________________________________________________________________\n")

    for i in data:
        doc = i.split('_')
        try:
            rno = doc[0]
            name = doc[1]
            age = doc[2]

            if sear == rno:
                print("Existing Record\n")
                print('Roll No:', rno)
                print('Name:', name)
                print('Age:', age)
                print()
                c += 1

        except IndexError:
            pass

    if c == 0:
        print("Record Not There")

    print("_________________________________________________________________\n")


def show_all():
    try:
        with open("record.txt", "r") as p:
            data = p.read()
            data = data.split(',')
    except FileNotFoundError:
        print("\nNo Files To Show (record.txt did not exist)")

    c = 0
    print()
    print("_________________________________________________________________\n")

    try:
        for i in data:
            doc = i.split('_')
            rno = doc[0]
            name = doc[1]
            age = doc[2]
            print('Member', c + 1, 'Details:')
            print('Roll No:', rno)
            print('Name:', name)
            print('Age:', age)
            print()
    except IndexError and UnboundLocalError:
        pass
    c += 1

    print("_________________________________________________________________\n")


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
