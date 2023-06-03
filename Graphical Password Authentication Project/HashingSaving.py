import hashlib
import sqlite3

class HashSave:
    def hash(self, text:str):
        # Hashes the given text and returns the hex hash
        digest = hashlib.sha512(bytes(text, 'utf-8')).hexdigest()
        return digest

    def save_in_db(self, username:str, password:str, symbol:str, symbol_string:str):
        # Stores the table and data in the database and returns 0 if data is stored otherwise -1
        try:
            db = sqlite3.connect("Save.db")
            db.execute('CREATE TABLE IF NOT EXISTS Passwords(username text, password text, symbol text, symbol_string text);')
            db.execute("INSERT INTO Passwords VALUES ('{}', '{}', '{}', '{}')".format(username, password, symbol, symbol_string))
            db.commit()
            db.close()
            return 0
        except Exception as e:
            return -1

    def read_db(self, username):
        # Reads the data when username is given
        data = ""
        try:
            db = sqlite3.connect("Save.db")
            cursor = db.cursor()
            cursor.execute("SELECT * FROM Passwords WHERE username='{}'".format(username))
            data = cursor.fetchall()
            cursor.close()
            db.close()
        except Exception as e:
            data = "Error"
        
        return data


if __name__ == '__main__':
    obj = HashSave()
    d = obj.hash("ben")
    print(d)
    x = obj.save_in_db('10', 'ben', 'azmuth', '10000')
    read = obj.read_db('10')
    print(read)
