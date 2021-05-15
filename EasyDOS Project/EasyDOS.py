import os.path
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import subprocess
import threading


# Window
root = Tk()
root.title("EasyDOS")
root.config(bg="#333333")
root.geometry("400x454")
root.iconbitmap(True, "images/icon.ico")

# Dos application path
dos_app_path = ""


# Commands
def open_dos():
    if var.get() == 0:
        new_thread('DOSBox\\DOSBox.exe -noconsole')
    elif var.get() == 1:
        new_thread('DOSBox\\DOSBox.exe -noconsole -fullscreen')


def open_dos_application():
    global dos_app_path
    dos_app_path = filedialog.askopenfilename()
    dos_app_path = str(dos_app_path).replace('/', '\\')

    if dos_app_path == "":
        messagebox.showerror("Error", "Select A Correct DOS Executable")
        return

    if var.get() == 0:
        new_thread('DOSBox\\DOSBox.exe "{}" -exit -noconsole'.format(dos_app_path))
    elif var.get() == 1:
        new_thread('DOSBox\\DOSBox.exe "{}" -exit -noconsole -fullscreen'.format(dos_app_path))


def open_dos_dir(event=""):
    path_str = str(dir_box.get())

    # Checking whether path is valid or not
    if not os.path.isdir(path_str):
        messagebox.showerror("Error", "Enter A Valid Directory")
        return

    if var.get() == 0:
        new_thread('DOSBox\\DOSBox.exe "{}" -noconsole'.format(path_str))
    elif var.get() == 1:
        new_thread('DOSBox\\DOSBox.exe "{}" -noconsole -fullscreen'.format(path_str))


def cmd_exec(path):
    # print(threading.active_count())
    cmd = subprocess.Popen(path, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    output = str(cmd.stdout.read() + cmd.stderr.read(), "utf-8")
    if output != "":
        messagebox.showerror("Error", output)


def new_thread(path):
    threading.Thread(target=cmd_exec, args=(path, )).start()


def helps():
    messagebox.showinfo("EasyDOS Help", "Default DOS Window Button : Will Open DOS With Default Directory.\n"
                                        "Load DOS Program Button: Will Open A Select Box To Run A DOS Program "
                                        "And That DOS Will Be Closed As Soon As You Quit The Program.\n"
                                        "Directory Mount Box : When You Enter A Directory And Press Enter Key Then DOS "
                                        "Will Get Opened In That Directory, Mounted As C: Drive.\n"
                                        "Fullscreen And Windowed Mode Radio Buttons : Are Used To Run DOS In Fullscreen"
                                        " Or In A Window.")


def dos_help():
    new_thread(".\\DOSBox\\Manual\\Manual.html")


def commands_help():
    new_thread("start https://www.dosbox.com/wiki/Commands")


def where_to():
    messagebox.showinfo("Where To Download DOS Programs", "Games: https://www.dosgames.com/\n"
                        "Programs: https://archive.org/details/softwarelibrary_msdos\n"
                        "Use google to get more programs and games")


def script_help():
    messagebox.showinfo("Where To Download DOS Programs", "To run many lines of DOS code then,\n"
                                                          "You can create a .BAT file "
                                                          "to execute many DOS commands at once")


def about_us():
    messagebox.showinfo("About Us", "EasyDOS Version 1.0\nDeveloped By Nikhil")


# Title label
title = Label(root, text="EasyDOS", font=("Times New Roman", 60), fg="#e6e8eb", bg="#333333")
title.pack(padx=10, pady=1)

# Open DOS button
open_dos_btn = Button(root, text="Default DOS Window",  command=open_dos, fg="#e6e8eb",
                      bg="#333333", activeforeground="white", activebackground="gray")
open_dos_btn.pack(pady=25)

# Load dosbox program
open_dos_app_img = PhotoImage(file="images/load.png")
open_dos_app = Button(root, text="Load DOS Application", image=open_dos_app_img, command=open_dos_application,
                      fg="#e6e8eb", bg="#333333", activebackground="gray")
open_dos_app.pack()

open_dos_app_lbl = Label(text="Load DOS Program", fg="#e6e8eb", bg="#333333")
open_dos_app_lbl.pack()

# Directory box
dir_box = Entry(root, width=56, fg="#e6e8eb", bg="#993e1c")
dir_box.bind("<Return>", open_dos_dir)
dir_box.bind("<Button-1>", lambda e: dir_box.delete(0, END))
dir_box.insert(0, "To Mount A Drive Type Directory Here And Press Enter Key")
dir_box.pack(pady=25)

# DOSBox fullscreen radio buttons
var = IntVar()

yes_fullscreen_rb = Radiobutton(root, variable=var, value=1, text="Fullscreen Mode", fg="#e6e8eb",
                                bg="#333333", selectcolor="black", activebackground="gray")
yes_fullscreen_rb.pack()

no_fullscreen_rb = Radiobutton(root, variable=var, value=0, text="Windowed Mode", fg="#e6e8eb",
                               bg="#333333", selectcolor="black", activebackground="gray")
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
am.add_command(label="About Us", command=about_us)


root.mainloop()
