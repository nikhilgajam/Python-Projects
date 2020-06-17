# DATABASE MANAGEMENT PROGRAM

import sqlite3


def create_database_table():
    try:
        connect = sqlite3.connect('Database.db')
        c = connect.cursor()

        c.execute('''CREATE TABLE Students (rno TEXT, name TEXT, age INT)''')
        connect.commit()
        connect.close()

        print("\nDatabase Table Created Successfully\n")
    except Exception as ex:
        print("Error:", ex)
        print("Type 5 To Display All Records")
        print()


def delete_database_table():
    try:
        connect = sqlite3.connect('Database.db')
        c = connect.cursor()

        c.execute('''DROP TABLE Students''')
        connect.commit()
        connect.close()

        print("\nDatabase Table Deleted Successfully\n")
    except Exception as ex:
        print("\nError:", ex)
        print("Type 5 To Display All Records")
        print()


def insert():
    try:
        print("INSERT\n")

        connect = sqlite3.connect('Database.db')
        c = connect.cursor()

        rno = input("Enter RNo: ")
        name = input("Enter Name: ")
        age = input("Enter Age: ")

        c.execute('''INSERT INTO Students (rno, name, age) VALUES (?, ?, ?)''', (rno, name, age))
        connect.commit()
        connect.close()

        print("\nInserted Into Database Successfully\n")
    except Exception as ex:
        print("\nError:", ex)
        print("Type 5 To Display All Records")
        print()


def update():
    try:
        print("UPDATE\n")

        connect = sqlite3.connect('Database.db')
        c = connect.cursor()

        r = input("Enter RNo To Update: ")

        c.execute('''SELECT * FROM Students WHERE rno='{}';'''.format(r))
        get = c.fetchone()

        print("RNo: {}\nName: {}\nAge: {}\n".format(get[0], get[1], get[2]))

        rno = input("Enter RNo: ")
        name = input("Enter Name: ")
        age = input("Enter Age: ")

        c.execute('''UPDATE Students SET rno = ? WHERE rno = ?''', (rno, r))
        c.execute('''UPDATE Students SET name = ? WHERE rno = ?;''', (name, r))
        c.execute('''UPDATE Students SET age = ? WHERE rno = ?;''', (age, r))
        connect.commit()
        connect.close()

        print("\nUpdated The Record In Database Successfully\n")
    except Exception as ex:
        print("\nError:", ex)
        print("Type 5 To Display All Records")
        print()


def delete():
    try:
        print("DELETE\n")

        connect = sqlite3.connect('Database.db')
        c = connect.cursor()

        rno = input("Enter RNo To Delete: ")

        c.execute('''SELECT * FROM Students WHERE rno='{}';'''.format(rno))
        get = c.fetchone()

        print("\nRNo: {}\nName: {}\nAge: {}".format(get[0], get[1], get[2]))

        c.execute('''DELETE FROM Students WHERE rno = ?;''', rno)
        connect.commit()
        connect.close()

        print("\nDeleted The Record In Database Successfully\n")
    except Exception as ex:
        print("\nError:", ex)
        print("Type 5 To Display All Records")
        print()


def search():
    try:
        print("SEARCH\n")

        connect = sqlite3.connect('Database.db')
        c = connect.cursor()

        rno = input("Enter RNo To Search: ")

        c.execute('''SELECT *, oid FROM Students WHERE rno=?''', rno)
        get = c.fetchone()

        print("\nRecord: {}\n\nRNo: {}\nName: {}\nAge: {}\n".format(get[3], get[0], get[1], get[2]))

        connect.close()
    except Exception as ex:
        print("\nError:", ex)
        print("Type 5 To Display All Records")
        print()


def display_all():
    try:
        print("DISPLAY ALL RECORDS\n")

        connect = sqlite3.connect('Database.db')
        c = connect.cursor()

        c.execute('''SELECT *, oid FROM Students''')
        records = c.fetchall()
        if not records:
            print("No Records To Display\n")

        for record in records:
            print("Record:", record[3])
            print("\nRNo: {}\nName: {}\nAge: {}\n\n".format(record[0], record[1], record[2]))

        connect.close()
    except Exception as ex:
        print("\nError:", ex)
        print("Type 5 To Display All Records")
        print()


# MAIN

print("Database Management Program\n")

print("1 - Insert new a record")
print("2 - Update a existing record")
print("3 - Delete a existing record")
print("4 - Search records ")
print("5 - Display all records")
print("6 - Create database table")
print("7 - Delete database table")
print("0 - Exit the program")

while True:

    try:
        sel = int(input("Enter: "))

        if sel == 1:
            insert()
        elif sel == 2:
            update()
        elif sel == 3:
            delete()
        elif sel == 4:
            search()
        elif sel == 5:
            display_all()
        elif sel == 6:
            create_database_table()
        elif sel == 7:
            delete_database_table()
        elif sel == 0:
            print("\nThanks for using")
            break
        else:
            print("\nEnter Instructed Numbers\n")

    except ValueError:
        print("\nEnter Only Numbers\n")
