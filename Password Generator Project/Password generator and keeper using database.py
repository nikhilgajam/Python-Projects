import sqlite3
import random
import pyperclip as pc

print("Password Generator And Keeper")


def password_generator():

    string = "1234567890!@#$%&*qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM."
    try:

        length = int(input("\nEnter Password Length (1-70): "))
        generate = "".join(random.sample(string, length))

        print("\n"+generate + "\t===> Copied to clipboard")
        pc.copy(generate)

    except ValueError:

        print("Enter Only Numbers")
        return

    except Exception as ex:
        print(ex)
        return

    x = input("\nDo you want to save this password (Yes/No): ")

    if "y" in x.lower():
        website = input("\nEnter Website And User ID Separated With (,)\n: ")

        connect = sqlite3.connect("manage.db")
        c = connect.cursor()

        try:

            c.execute('''CREATE TABLE IF NOT EXISTS Manage (User TEXT, Get TEXT)''')

            c.execute('''INSERT INTO Manage (User, Get) VALUES (?, ?)''', (website, generate))
            connect.commit()
            connect.close()
            print("\nSaved Successfully")
        except Exception as ex:
            print("Error:", ex)

    else:
        print("\nO.K Done")


while True:
    password_generator()

    get = input("\nGenerate Another Password? (Yes/No): ")
    if 'y' in get.lower():
        password_generator()
    else:
        print("\nDone")
        break
