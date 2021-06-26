import os
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter import simpledialog
import subprocess
import threading
import sqlite3


# Window
root = Tk()
root.title("EasyDOS")
root.config(bg="#333333")
root.geometry("400x400")
root.iconbitmap(True, "images/icon.ico")

# Dos application path
dos_app_path = ""


# Commands

def open_dos(event=""):
    # This code will be executed when open DOS default window button is clicked
    if screen_var.get() == 0:
        new_thread('DOSBox\\DOSBox.exe -noconsole')
    elif screen_var.get() == 1:
        new_thread('DOSBox\\DOSBox.exe -noconsole -fullscreen')


def open_dos_application(event=""):
    # This will be executed when open application button is clicked
    global dos_app_path
    dos_app_path = filedialog.askopenfilename()
    dos_app_path = str(dos_app_path).replace('/', '\\').lower()

    if dos_app_path == "":
        messagebox.showerror("Error", "Select A Correct DOS Executable With Extension (.exe) or (.com) or (.bat)")
        return

    if dos_app_path.find(".exe") > -1 or dos_app_path.find(".com") > -1 or dos_app_path.find(".bat") > -1:
        if screen_var.get() == 0:
            new_thread('DOSBox\\DOSBox.exe "{}" -exit -noconsole'.format(dos_app_path))
        elif screen_var.get() == 1:
            new_thread('DOSBox\\DOSBox.exe "{}" -exit -noconsole -fullscreen'.format(dos_app_path))
    else:
        messagebox.showerror("Error", "Select A Correct DOS Executable With Extension (.exe) or (.com) or (.bat)")
        return


def open_dos_dir(event=""):
    # This will be executed when enter pressed in Mount Drive Box
    path_str = str(dir_box.get()).replace('/', '\\')

    # Checks whether path is valid or not
    if not os.path.isdir(path_str):
        messagebox.showerror("Error", "Enter A Valid Directory")
        return

    if screen_var.get() == 0:
        new_thread('DOSBox\\DOSBox.exe "{}" -noconsole'.format(path_str))
    elif screen_var.get() == 1:
        new_thread('DOSBox\\DOSBox.exe "{}" -noconsole -fullscreen'.format(path_str))


def cmd_exec(path):
    # CMD commands will executed
    # print(threading.active_count())
    cmd = subprocess.Popen(path, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    # output = str(cmd.stdout.read() + cmd.stderr.read(), "utf-8")
    output = str(cmd.stderr.read(), "utf-8")
    if output != "":
        messagebox.showerror("Error", output)


def new_thread(path):
    # This create a new thread
    threading.Thread(target=cmd_exec, args=(path, )).start()


def settings(event=""):
    # This is used to open the settings window
    top = Toplevel(root, bg="#333333")
    top.title("EasyDOS Settings")
    top.resizable(0, 0)
    top.focus()
    top_title = Label(top, text="EasyDOS Settings", font=("Times New Roman", 40), fg="#e6e8eb", bg="#333333")
    top_title.pack(pady=10)

    def reset_option(x):
        if x == 1:
            new_thread('cd DOSBox && "Reset Options"')
            messagebox.showinfo("EasyDOS", "Options Reset Completed")
            top.focus()
        elif x == 2:
            new_thread('cd DOSBox && "Reset KeyMapper"')
            messagebox.showinfo("EasyDOS", "KeyMapper Reset Completed")
            top.focus()

    set_options_btn = Button(top, text="Options",
                             command=lambda: new_thread('cd DOSBox && "DOSBox 0.74-3 Options"'),
                             fg="#e6e8eb", bg="#333333", activeforeground="white", activebackground="gray")
    set_options_btn.bind("<Return>", lambda x: new_thread('cd DOSBox && "DOSBox 0.74-3 Options"'))
    set_options_btn.pack(pady=3)

    set_reset_opt_btn = Button(top, text="Reset Options", command=lambda: reset_option(1),
                               fg="#e6e8eb", bg="#333333", activeforeground="white", activebackground="gray")
    set_reset_opt_btn.bind("<Return>", lambda x: reset_option(1))
    set_reset_opt_btn.pack(pady=3)

    set_reset_key_btn = Button(top, text="Reset KeyMapper", command=lambda: reset_option(2),
                               fg="#e6e8eb", bg="#333333", activeforeground="white", activebackground="gray")
    set_reset_key_btn.bind("<Return>", lambda x: reset_option(2))
    set_reset_key_btn.pack(pady=3)

    set_scr_btn = Button(top, text="Screenshots & Recordings",
                         command=lambda: new_thread('cd DOSBox && "Screenshots & Recordings"'),
                         fg="#e6e8eb", bg="#333333", activeforeground="white", activebackground="gray")
    set_reset_key_btn.bind("<Return>", lambda x: new_thread('cd DOSBox && "Screenshots & Recordings"'))
    set_scr_btn.pack(pady=3)


def program_manager(event=""):
    # This is used to open program manager window
    # Creating a directory in appdata/roaming/
    data_path = os.environ["appdata"] + "\\EasyDOS"
    if not os.path.exists(data_path):
        os.makedirs(data_path)

    # Connecting to the database and creating a table
    c = sqlite3.connect(data_path + "\\data.db")
    c.execute("CREATE TABLE IF NOT EXISTS Data(name TEXT PRIMARY KEY, path TEXT)")

    # Commands

    def add(e=""):
        # Adds the program title and path to database
        name_str = simpledialog.askstring("EasyDOS", "Enter Program Title: ")
        if name_str == "" or name_str is None:
            messagebox.showerror("Error", "Enter A Name In Popup Box")
            list_box.focus()
            return

        temp = str(filedialog.askopenfilename()).lower().replace("/", "\\")
        list_box.focus()
        if temp == "":
            messagebox.showerror("Error", "Select A Correct DOS Executable With Extension (.exe) or (.com) or (.bat)")
            list_box.focus()
            return

        if temp.find(".exe") > -1 or temp.find(".com") > -1 or temp.find(".bat") > -1:
            try:
                c.execute("INSERT INTO Data(name, path)VALUES('{}', '{}')".format(name_str.lower().title(), temp))
                c.commit()
                update_box()
            except Exception:
                messagebox.showwarning("Warning", "This Title Already Exists Try Another One")
                list_box.focus()
        else:
            messagebox.showerror("Error", "Select A Correct DOS Executable With Extension (.exe) or (.com) or (.bat)")
            list_box.focus()
            return

    def delete(e=""):
        # Deletes the program path from database
        temp = str(list_box.get(ACTIVE))
        c.execute('DELETE FROM Data WHERE name = "{}"'.format(temp))
        c.commit()
        update_box()

    def load(e=""):
        # Loads the program with dosbox
        try:
            temp = str(list_box.get(ACTIVE))
            temp = str(c.execute('SELECT path FROM Data WHERE name = "{}"'.format(temp)).fetchall()[0][0])

            # Checks whether path exists or not
            if not os.path.exists(temp):
                messagebox.showerror("Error", "Directory or file not found")
                list_box.focus()
                return

            if screen_var.get() == 0:
                new_thread('DOSBox\\DOSBox.exe "{}" -noconsole'.format(temp))
            elif screen_var.get() == 1:
                new_thread('DOSBox\\DOSBox.exe "{}" -noconsole -fullscreen'.format(temp))
            close()
        except IndexError:
            messagebox.showerror("Error", "ADD A New Program If Program Box Is Empty And Then LOAD")
            list_box.focus()

    def update_box():
        # Updates the listbox
        list_box.delete(0, END)
        temp = c.execute("SELECT name FROM Data ORDER BY name").fetchall()
        for i, j in enumerate(temp):
            list_box.insert(i, str(j[0]))

    def close():
        # Used to close the program manager and also closes the database
        c.close()
        top.destroy()

    # Window settings
    top = Toplevel(root, bg="#333333")
    top.title("EasyDOS Program Manager")
    top_title = Label(top, text="   Program Manager   ", font=("Times New Roman", 29), fg="#e6e8eb", bg="#333333")
    top_title.pack(pady=10, fill=BOTH)
    top.protocol("WM_DELETE_WINDOW", close)

    # Listbox which shows program titles and scrollbar
    list_frame = Frame(top, bg="#333333")
    list_frame.pack(fill=BOTH, expand=TRUE, padx=3)

    scroll_bar = Scrollbar(list_frame, orient="vertical", bg="#333333", troughcolor="#333333")
    scroll_bar.pack(side=RIGHT, fill=Y, anchor=NE)

    list_box = Listbox(list_frame, fg="#e6e8eb", bg="#333333", yscrollcommand=scroll_bar.set,
                       font=("Times New Roman", 15), selectbackground="#993e1c")
    scroll_bar.config(command=list_box.yview)
    list_box.pack(fill=BOTH, expand=TRUE)
    list_box.bind("<Insert>", add)
    list_box.bind("<Return>", load)
    list_box.bind("<Delete>", delete)
    list_box.focus()

    # Buttons
    buttons = Frame(top, bg="#333333")
    buttons.pack()

    load_btn = Button(buttons, text="LOAD", command=load, fg="#e6e8eb", bg="#333333",
                      activeforeground="white", activebackground="gray")
    load_btn.bind("<Return>", load)
    load_btn.grid(row=1, column=0, padx=6, pady=6)

    add_btn = Button(buttons, text=" ADD ", command=add, fg="#e6e8eb", bg="#333333",
                     activeforeground="white", activebackground="gray")
    add_btn.bind("<Return>", add)
    add_btn.grid(row=1, column=1, padx=6, pady=6)

    del_btn = Button(buttons, text=" DEL ", command=delete, fg="#e6e8eb", bg="#333333",
                     activeforeground="white", activebackground="gray")
    del_btn.bind("<Return>", delete)
    del_btn.grid(row=1, column=2, padx=6, pady=6)
    update_box()


def helps():
    # This will open the help window
    messagebox.showinfo("EasyDOS Help", "Program Manager Button : You Can Add Programs To Browse Box To Access"
                                        "Them Later Quickly.\n"
                                        "Load DOS Program Button: Will Open A Select Box To Run A DOS Program "
                                        "And That DOS Will Be Closed As Soon As You Quit The Program.\n"
                                        "Default DOS Window Button : Will Open DOS With Default Directory.\n"
                                        "Drive Mount Box : When You Paste A Path(CTRL + V) And Press Enter Key "
                                        "Then DOS Will Get Opened In That Directory, Mounted As C: Drive.\n"
                                        "Fullscreen And Windowed Mode Radio Buttons : Used To Run DOS In Fullscreen"
                                        " Or In A Window.\n"
                                        "Settings Menu Button : With This You Can Change DOSBox Settings.")


def dos_help():
    # This will open the dos help window
    new_thread(".\\DOSBox\\Manual\\Manual.html")


def commands_help():
    # This will open commands help in browser
    new_thread("start https://www.dosbox.com/wiki/Commands")


def where_to():
    # This will open the window which suggests some websites to download DOS programs and games
    messagebox.showinfo("Where To Download DOS Programs", "Games: https://www.dosgames.com/\n"
                                                          "Programs: https://archive.org/details/softwarelibrary_msdos\n"
                                                          "Use google to get more programs and games.")


def script_help():
    # This will open a window which will tell how to run multiple DOS commands
    messagebox.showinfo("How To Run Script", "To run many lines of DOS code then,\n"
                                             "You can create a .BAT file "
                                             "to execute many DOS commands at once.")


def about_us():
    # This will open about us window
    messagebox.showinfo("About Us", "EasyDOS Version 1.0\nDeveloped By Nikhil")


# Title label
title = Label(root, text="EasyDOS", font=("Times New Roman", 56), fg="#e6e8eb", bg="#333333")
title.pack(padx=10, pady=1)

# Program manager
program_btn = Button(root, text="Program Manager",  command=program_manager, fg="#e6e8eb",
                     bg="#333333", activeforeground="white", activebackground="gray")
program_btn.bind("<Return>", program_manager)
program_btn.pack(pady=20)

# Load dosbox program
open_dos_app_img = PhotoImage(file="images/loads.png")

open_dos_app = Button(root, text="Load DOS Application", image=open_dos_app_img, command=open_dos_application,
                      fg="#e6e8eb", bg="#333333", activebackground="gray")
open_dos_app.bind("<Return>", open_dos_application)
open_dos_app.pack()

open_dos_app_lbl = Label(text="Load DOS Program", fg="#e6e8eb", bg="#333333")
open_dos_app_lbl.pack()

# Open DOS button
open_dos_btn = Button(root, text="Default DOS Window",  command=open_dos, fg="#e6e8eb",
                      bg="#333333", activeforeground="white", activebackground="gray")
open_dos_btn.bind("<Return>", open_dos)
open_dos_btn.pack(pady=11)

# Directory box
dir_box = Entry(root, width=56, fg="#e6e8eb", bg="#993e1c")
dir_box.bind("<Return>", open_dos_dir)
dir_box.bind("<Button-1>", lambda e: dir_box.delete(0, END))
dir_box.insert(0, "To Mount A Drive, Paste The Path Here And Press Enter Key.")
dir_box.pack(pady=11)

# DOSBox fullscreen radio buttons
screen_var = IntVar()

yes_fullscreen_rb = Radiobutton(root, variable=screen_var, value=1, text="Fullscreen Mode", fg="#e6e8eb",
                                bg="#333333", selectcolor="black", activebackground="gray")
yes_fullscreen_rb.bind("<Return>", lambda x: yes_fullscreen_rb.invoke())
yes_fullscreen_rb.pack()

no_fullscreen_rb = Radiobutton(root, variable=screen_var, value=0, text="Windowed Mode", fg="#e6e8eb",
                               bg="#333333", selectcolor="black", activebackground="gray")
no_fullscreen_rb.bind("<Return>", lambda x: no_fullscreen_rb.invoke())
no_fullscreen_rb.invoke()
no_fullscreen_rb.pack(pady=3)

# Menu
m = Menu(root)
root.config(menu=m)

am = Menu(m, tearoff=0)
m.add_cascade(label="Help", menu=am)
am.add_command(label="Help", command=helps)
am.add_command(label="DOS Help", command=dos_help)
am.add_command(label="Commands", command=commands_help)
am.add_command(label="Where To Download DOS Programs", command=where_to)
am.add_command(label="How To Run Script", command=script_help)

sm = Menu(m, tearoff=0)
m.add_cascade(label="Settings", menu=sm)
sm.add_command(label="Open Settings", command=settings)

abm = Menu(m, tearoff=0)
m.add_cascade(label="About", menu=abm)
abm.add_command(label="About Us", command=about_us)

# To place window in the center of the screen
root.eval('tk::PlaceWindow . center')

# Mainloop
root.mainloop()
