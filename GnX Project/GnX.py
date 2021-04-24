from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pyperclip
import sqlite3
import random
import os


# Storage
UN = ""


# Commands
def sign_change():
    if var.get() == 1:
        show['text'] = "Master Sign In\n"
    elif var.get() == 2:
        show['text'] = "Master Sign Up\n"


def sign_ver(event=""):
    global UN
    connect = sqlite3.connect("ud/users.db")

    if var.get() == 1:
        if un_box.get() == "" or pw_box.get() == "":
            messagebox.showwarning("Warning", "Enter Your Username And Password")
            return

        try:
            get = connect.execute("SELECT * FROM Users").fetchall()
        except:
            messagebox.showerror("Error", "Sign Up To Create An Account")
            return
        ok = False
        for i, j in get:
            if i == un_box.get() and j == pw_box.get():
                ok = True
                break
        if ok:
            UN = un_box.get()
            root.destroy()
            account()
        else:
            messagebox.showerror("Error", "Enter Correct Username And Password\n"
                                          "If You Don't Have An Account Click On Sign Up Radio Button")

    elif var.get() == 2:
        try:
            connect.execute("CREATE TABLE IF NOT EXISTS Users(un TEXT PRIMARY KEY, pw TEXT)")
            connect.execute("INSERT INTO Users(un, pw) VALUES (?, ?)", (un_box.get(), pw_box.get()))
            connect.commit()
        except:
            messagebox.showwarning("Warning", "This Username Already Exists Use Another")
            connect.close()
            return

        sign_in.invoke()

    connect.close()


def account():
    # Window
    win = Tk()
    win.title("GnX")
    # Highlighting the win window
    win.after(1, lambda: win.focus_force())
    win.iconbitmap(True, "images/icon.ico")

    # Opening the database
    connect = sqlite3.connect("ud/data.db")
    connect.execute("CREATE TABLE IF NOT EXISTS {}(un TEXT PRIMARY KEY, pw TEXT)".format(UN))

    # Command
    def saves(event=""):
        name = u_box.get()
        if name == "":
            messagebox.showerror("Error", "Enter A Name Or Website Or Username")
            return

        # Checking whether the inserting username is present or not
        x = connect.execute("SELECT DISTINCT 1 FROM {} WHERE un='{}'".format(UN, name)).fetchone()
        # If present terminate the execution
        if x is not None:
            messagebox.showerror("Error", "This Username Or Website Name Already Exists Use Another")
            return

        # Calling password generator
        g = generator(s_box.get())

        # If generator returns None then we need to terminate this saves
        if g is None:
            return

        try:
            connect.execute("INSERT INTO {}(un, pw) VALUES ('{}', '{}')".format(UN, name, str(g)))
            connect.commit()
        except:
            messagebox.showerror("Error", "This Username Or Website Name Already Exists Use Another")
            return

        text.insert(END, u_box.get() + " | " + str(g) + "\n")

    # Text
    vscroll = Scrollbar(win, orient=VERTICAL)
    vscroll.pack(side=RIGHT, fill=Y, anchor=NE)
    text = Text(win, wrap="word", undo=True, yscrollcommand=vscroll.set)
    text.pack(fill=BOTH, expand=TRUE)
    vscroll.config(command=text.yview)

    # Starting Message
    text.insert(1.0, "Username | Password\n")

    # Inserts the content from database to text box
    get = connect.execute("SELECT * FROM {}".format(UN))
    for i, j in get:
        if i is None or j is None:
            continue
            # If i or j is None then it causes error that's why we are avoiding those nones
        text.insert(END, i + " | " + j + "\n")

    boxes = Frame(win)
    boxes.pack()

    # Name Or Website
    u = ttk.Label(boxes, text="Username: ")
    u.grid(row=0, column=0, padx=10)

    u_box = ttk.Entry(boxes)
    u_box.focus()
    u_box.grid(row=0, column=1, padx=10, pady=6)
    u_box.bind("<Return>", saves)

    # Size
    s = ttk.Label(boxes, text="Size (8-70): ")
    s.grid(row=0, column=2, padx=10)

    s_box = ttk.Entry(boxes)
    s_box.insert(0, "8")
    s_box.grid(row=0, column=3, padx=10)
    s_box.bind("<Return>", saves)

    # Save Button
    save = ttk.Button(boxes, text="Save", command=saves)
    save.grid(row=0, column=4)

    win.mainloop()
    # Closing the database connection
    connect.close()


def generator(length):
    string = "1234567890!@#$%&*qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM."
    try:
        length = int(length)
        if length < 8 or length > 70:
            messagebox.showerror("Error", "Enter Numbers in range (8- 70)")
            return

        generated = "".join(random.sample(string, length))

        # If yes pressed the copies the password to clipboard
        x = messagebox.askyesno("Asking!", "Do You Want To Copy The Password To Clip Board")
        if x:
            pyperclip.copy(generated)
        return generated

    except ValueError:
        messagebox.showerror("Error", "Enter Only Numerical Values In Size Box")
        return


# Main

root = Tk()
root.title("GnX")
root.geometry("350x350")
root.iconbitmap(True, "images/icon.ico")
root.resizable(0, 0)

# Title

title = Label(root, text="GnX", font="Mistral 80")
title.pack()

# Creating ud directory if not exists

try:
    os.mkdir("ud")
except FileExistsError:
    pass

# Sign In / Sign Up

show = Label(root, text="Master Sign In\n", font="Calibri 20")
show.pack()

# Group frame

group = Frame(root)
group.pack()

# Username Box

un = ttk.Label(group, text="Username: ")
un.grid(row=0, column=0)

un_box = ttk.Entry(group)
un_box.focus()
un_box.grid(row=0, column=1, padx=10, pady=6)

# Password Box

pw = ttk.Label(group, text="Password: ")
pw.grid(row=2, column=0)

pw_box = ttk.Entry(group, show="*")
pw_box.grid(row=2, column=1)
pw_box.bind("<Return>", sign_ver)

# Confirm Button

confirm = ttk.Button(root, text="Confirm", command=sign_ver)
confirm.pack(pady=11)

# RadioButton Variable

var = IntVar()

# RadioButton Sign In

sign_in = ttk.Radiobutton(root, text="Sign In", variable=var, value=1, command=sign_change)
sign_in.invoke()
sign_in.pack()

# RadioButton Sign Up

sign_up = ttk.Radiobutton(root, text="Sign Up", variable=var, value=2, command=sign_change)
sign_up.pack()

root.mainloop()