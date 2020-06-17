# DATABASE TO MANAGE PHOTOS, MUSIC AND OTHER DATA PROGRAM

import sqlite3


# Class


class DataBase:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connect = sqlite3.connect(self.db_name)
        self.c = self.connect.cursor()
        self.path = ""

        print("Database To Manage Photos, Music And Other Data\n")

        print("1. Insert data")
        print("2. Remove data")
        print("3. Update metadata")
        print("4. Search data")
        print("5. Show all data")
        print("6. Export data")
        print("7. Create data table")
        print("8. Delete data table")
        print("9. Optimise database")
        print("0. Quit")

        while True:

            try:
                self.choice = int(input("\nEnter: "))

                if self.choice == 1:
                    self.insert_data()
                elif self.choice == 2:
                    self.delete_data()
                elif self.choice == 3:
                    self.update_metadata()
                elif self.choice == 4:
                    self.search_data()
                elif self.choice == 5:
                    self.show_all_data()
                elif self.choice == 6:
                    self.export_data()
                elif self.choice == 7:
                    self.create_data_table()
                elif self.choice == 8:
                    self.delete_data_table()
                elif self.choice == 9:
                    self.optimise_database()
                elif self.choice == 0:
                    break
                else:
                    print("Enter Mentioned Numbers Only")

            except ValueError:
                print("Enter Numbers Only")

    def insert_data(self):
        try:
            print("\nINSERT DATA\n")

            print("NOTE: Enter Name With Extension like pic.jpg\n")
            name = input("Enter Name: ")
            d_type = input("Enter Type Of Data: ")
            date = input("Enter Date: ")
            data = input("Enter Data Path: ")

            bin_data = self.import_data(data)

            self.c.execute('''INSERT INTO Data (name, type, date, data) VALUES (?, ?, ?, ?)''', (name, d_type, date,
                                                                                                 bin_data))

            self.connect.commit()

            print("\nData Inserted Into Database Successfully")

        except Exception as ex:
            print("\nError:", ex)

    def delete_data(self):
        try:
            print("\nDELETE DATA\n")

            sno = input("Enter Serial No To Delete: ")

            self.c.execute('''DELETE FROM Data WHERE oid=?''', sno)

            self.connect.commit()

            print("\nData In Database Deleted Successfully")

        except Exception as ex:
            print("\nError:", ex)

    def update_metadata(self):
        try:
            print("\nUPDATE META DATA\n")

            print("NOTE: You Can See Serial No In Show All\n")
            sno = int(input("Enter Serial No To Update: "))
            name = input("Enter Name To Update: ")

            self.c.execute('''SELECT *, oid FROM Data WHERE name="{}"'''.format(name))
            gets = self.c.fetchall()

            count = 0

            for get in gets:
                if get[4] == sno:

                    count += 1

                    print("\nData Serial No:", get[4])
                    print("Name:", get[0], "\nType:", get[1], "\nDate:", get[2])

                    print("NOTE: Enter Name With Extension like pic.jpg\n")
                    new_name = input("\nEnter New Name: ")
                    new_d_type = input("Enter New Data Type: ")
                    new_date = input("Enter New Date: ")

                    self.c.execute('''UPDATE Data SET name="{}" WHERE name="{}"'''.format(new_name, name))
                    self.c.execute('''UPDATE Data SET type="{}" WHERE name="{}"'''.format(new_d_type, name))
                    self.c.execute('''UPDATE Data SET date="{}" WHERE date="{}"'''.format(new_date, name))

                    self.connect.commit()

                    print("\nMetadata In Database Updated Successfully")

            if count == 0:
                print("\nData not found")

        except Exception as ex:
            print("\nError:", ex)

    def search_data(self):
        try:
            print("\nSEARCH DATA\n")

            name = input("Enter Name: ")

            self.c.execute('''SELECT *, oid FROM Data WHERE name="{}"'''.format(name))
            gets = self.c.fetchall()
            if not gets:
                print(name, "is not found")
                return

            for get in gets:
                print("\nData Serial No:", get[4])
                print("Name:", get[0], "\nType:", get[1], "\nDate:", get[2])

            self.connect.commit()

        except Exception as ex:
            print("\nError:", ex)

    def show_all_data(self):
        try:
            print("\nSHOW ALL DATA\n")

            self.c.execute("SELECT *, oid FROM Data")
            records = self.c.fetchall()

            if not records:
                print("No Records To Display")
                return

            for record in records:
                print("Data Serial No:", record[4])
                print("Name:", record[0], "\nType:", record[1], "\nDate:", record[2])
                print()

        except Exception as ex:
            print("\nError:", ex)

    def import_data(self, path):
        try:
            self.path = path
            with open(path, "rb") as p:
                data = p.read()
                return data

        except Exception as ex:
            print("\nError:", ex)

    def export_data(self):
        try:
            print("\nEXPORT DATA\n")

            print("NOTE: You Can See Serial No In Show All\n")
            sno = int(input("Enter Serial No To Export: "))
            name = input("Enter Name To Export: ")

            self.c.execute('''SELECT *, oid FROM Data WHERE name="{}"'''.format(name))
            gets = self.c.fetchall()

            count = 0

            for get in gets:
                if get[4] == sno:
                    print("Name:", get[0], "\nType:", get[1], "\nDate:", get[2])
                    data = get[3]
                    count += 1

                    with open(get[0], "wb") as p:
                        p.write(data)

                    print("\nData In Database Exported Successfully")

            if count == 0:
                print("\nData not found")

        except Exception as ex:
            print("Error:", ex)

    def create_data_table(self):
        try:
            print("\nCREATE DATA TABLE\n")

            self.c.execute('''CREATE TABLE Data (name TEXT, type TEXT, date TEXT, data BLOB)''')
            self.connect.commit()

            print("Data Table Created Successfully")

        except Exception as ex:
            print("\nError:", ex)

    def delete_data_table(self):
        try:
            print("\nDELETE DATA TABLE\n")

            get = input("\nThis is going to wipe all your data in database\nAre You Sure To Proceed?(Yes/No): ")
            if get.lower() == 'no':
                print("\nData Table Not Deleted")
                return

            self.c.execute('''DROP TABLE Data''')
            self.connect.commit()

            print("Data Table Deleted Successfully")

        except Exception as ex:
            print("\nError:", ex)

    def optimise_database(self):
        self.c.execute('''VACUUM''')
        print("\nDatabase Is Optimized")


# Main

db = DataBase("Data.db")
