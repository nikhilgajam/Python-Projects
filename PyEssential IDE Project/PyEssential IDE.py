from tkinter import *
from tkinter import messagebox as tm
from tkinter import filedialog
from tkinter.font import Font
from tkinter import simpledialog
from datetime import datetime
import time
import os

root = Tk()
root.title("PyEssential IDE")
root.iconbitmap(True, "images/icon.ico")
root.geometry("942x542")

path = ""
count = 0
theme = ""


# Commands


def opens(event=""):
    global path, count

    path = filedialog.askopenfilename(title="Open", filetype=(("All Files", "*.*"),))
    if path == "":
        return
    else:
        text = editor.get(1.0, END)
        editor.index(1.1)
        pos = editor.index(INSERT)
        if pos == "1.0" or count > 0:
            with open(path, 'r', encoding="ansi") as p:
                text = p.read()
            editor.delete(1.0, END)
            editor.insert(1.0, text)
            count = 0
            root.title("PyEssential IDE  –  " + os.path.basename(path))
        else:
            ask = tm.askquestion("PyEssential IDE", "Do you want to save this text?")
            if ask == 'yes':
                save_as()
                text = path.read()
                editor.delete(1.0, END)
                editor.insert(1.0, text)
                count = 0
                root.title("PyEssential IDE  –  " + os.path.basename(path))
            else:
                with open(path, "r", encoding="ansi") as p:
                    text = p.read()

                if text is None:
                    return
                else:
                    editor.delete(1.0, END)
                    editor.insert(1.0, text)
                    count = 0
                    root.title("PyEssential IDE  –  " + os.path.basename(path))


def new(event=""):
    editor.mark_set(INSERT, END)
    pos = editor.index(INSERT)

    if pos == "1.0":
        editor.delete(1.0, END)
    else:
        ask = tm.askyesnocancel("PyEssential IDE", "Do you want to save this text?")
        if ask is True:
            get = save_as()
            if get is True:
                editor.delete(1.0, END)

        elif ask is False:
            editor.delete(1.0, END)

    root.title("PyEssential IDE")


def save_as():
    global path, count
    saveas = filedialog.asksaveasfile(initialfile="PyEssential.py", defaultextension=".py",
                                      filetype=(("Python", "*.py"), ("Text Document", "*.txt"), ("All Files", "*.*")))
    if saveas is None:
        return None
    else:
        saveas = saveas.name
        path = saveas
        text = editor.get(1.0, END)
        with open(saveas, 'w', encoding="ansi") as p:
            p.write(text)
        count += 1
        root.title("PyEssential IDE  –  " + os.path.basename(path))
        return True


def save(event=""):
    global path, count

    if path == "":
        save_as()
    else:
        saves = editor.get(1.0, END)
        os.remove(path)
        with open(path, "w") as p:
            p.write(str(saves))
            count = 1


def search(event=""):
    ask = simpledialog.askstring("Search", "Enter the word to search")
    get = editor.get(1.0, END)
    editor.focus_set()

    if ask is None:
        return
    elif ask == "":
        tm.showwarning("Search", "Enter Any Word")
    else:
        ask = str(ask).lower()
        get = str(get).lower()
        show = get.count(ask)
        tm.showinfo("Search", "'" + ask.capitalize() + "'" + " Repeated " + str(show) + " Time(s) ")


def counts(event=""):
    get = str(editor.get(1.0, END))
    letter_count = word_count = space_count = line_count = every_char = 0
    editor.mark_set(INSERT, 1.0)

    for i in get:
        every_char += 1

        if i != " " and i != "\n" and i != "\t":
            letter_count += 1
        elif i == "\n":
            line_count += 1
        else:
            space_count += 1

    get = get.split(" ")

    for i in get:
        word_count += 1

    if get[0] == "\n":
        word_count = 0

    tm.showinfo("Count", "All Character Count: " + str(every_char) + "\n" + "Word Count: " + str(
        word_count) + "\n" + "Letter Count: " + str(letter_count) + "\n" + "Space Count: " + str(
        space_count) + "\n" + "Line count: " + str(line_count))


def close():
    editor.mark_set(INSERT, END)
    pos = editor.index(INSERT)

    if count == 0:
        if pos == "1.0":
            root.destroy()
        else:
            ask = tm.askyesnocancel("PyEssential IDE", "Do you want to save this text?")
            if ask is True:
                get = save_as()
                if get is True:
                    root.destroy()
            elif ask is False:
                root.destroy()

    else:
        root.destroy()


def time_date(event=""):
    c = time.ctime(time.time())
    d = datetime.strptime(c[11:16], "%H:%M")
    d = d.strftime("%I:%M %p")
    d = d[:-3] + c[16:19] + d[5:]

    time__date = " " + d + "  " + c[:4] + "- " + c[8:10] + "/" + c[4:7] + "/" + c[20:] + " "
    editor.insert(END, time__date)


def helps():
    tm.showinfo("About Us", "PyEssential IDE Is Developed By Nikhil")


def cut():
    copy()
    editor.delete("sel.first", "sel.last")


def copy():
    editor.clipboard_clear()
    editor.clipboard_append(editor.selection_get())


def paste():
    editor.insert(INSERT, editor.clipboard_get())


def select_all():
    editor.tag_add(SEL, "1.0", END)
    editor.mark_set(INSERT, 1.0)
    editor.see(INSERT)


def adjust_text_size():
    global text_size

    ask = simpledialog.askinteger("Text Size", "Enter (1-100), Default = 10")
    if ask is None:
        return

    else:
        tst['size'] = ask
        text_size = ask
        update_status_bar()

    editor.focus_set()


current_text = "Current : Lucida Console"


def adjust_text_type():
    global current_text
    ask = simpledialog.askstring("Text Type",
                                 "Enter Any Correct Text Type\n\nDefault : Lucida Console\n" + current_text)
    if ask is None:
        return
    else:
        tst['family'] = ask
        current_text = "Current : " + ask

    editor.focus_set()


current_style = "Current :  Normal,Roman,0,0"


def adjust_text_style():
    global current_style
    ask = simpledialog.askstring("Text Style", "Enter : \nWeight :  Bold | Normal\nSlant :  Italic | Roman\n"
                                               "Underline :  1 | 0\nOverstrike :  1 | 0\n\nDefault :  Normal,Roman,0,0\n"
                                 + current_style)
    if ask is None:
        return
    else:
        ask = str(ask)
        ask = ask.split(',')
        tst['weight'] = ask[0].lower()
        tst['slant'] = ask[1].lower()
        tst['underline'] = int(ask[2])
        tst['overstrike'] = int(ask[3])

        current_style = "Current :  " + ask[0].capitalize() + "," + ask[1].capitalize() + "," + ask[2] + "," + ask[3]

    editor.focus_set()


def adjust_wrap():
    if wrap.get() == 1:
        editor['wrap'] = "word"
        hscroll['width'] = 0
    else:
        editor['wrap'] = NONE
        hscroll['width'] = 16


def themes():
    global theme
    if dark.get() == "Default":
        editor['bg'] = "white"
        editor['insertbackground'] = "black"
        editor['fg'] = "black"
        theme = ""
        statusBar.configure(bg="#e1e1e1", fg="black")
    elif dark.get() == "Dark Theme":
        editor['bg'] = "#333333"
        editor['insertbackground'] = "white"
        editor['fg'] = "#e6e8eb"
        theme = "Dark Theme    |    "
        statusBar.configure(bg="#333334", fg="#e6e8eb")
    elif dark.get() == "Great Green":
        editor['bg'] = "#2b3d40"
        editor['insertbackground'] = "#e6e8eb"
        editor['fg'] = "white"
        theme = "Great Green    |    "
        statusBar.configure(bg="#3b3d40", fg="#e6e8eb")
    elif dark.get() == "Violet":
        editor['bg'] = "#2c4079"
        editor['insertbackground'] = "white"
        editor['fg'] = "white"
        theme = "Violet    |    "
        statusBar.configure(bg="#1c4079", fg="white")

    update_status_bar()


def set_status():
    if status.get() == 0:
        statusBar.pack_forget()
    else:
        tm.showinfo("PyEssential IDE", "Restart PyEssential IDE")


def tab(event=""):
    editor.insert(INSERT, " " * 4)
    return 'break'


def build_run(event=""):
    if path != "":
        save()
    else:
        tm.showinfo("PyEssential IDE", "Save the file to build")
        return
    os.system("cmd /c start cmd.exe /K \"Python\\python.exe \"" + path + "\" && title PyEssential IDE && pause && exit\"")


def update_status_bar(event=""):
    row, col = editor.index(INSERT).split('.')
    col = int(col)
    col += 1
    statusBar['text'] = theme + "Size  :  " + str(text_size) + "    |    ANSI    |    " + "Line : " + row + " | " + \
                        "Col : " + str(col) + " "

    x_pos = hscroll.get()
    if x_pos == (0.0, 1.0):
        hscroll['width'] = 0
    else:
        hscroll['width'] = 16


def popup(event):
    popup_menu.post(event.x_root, event.y_root)  # Popup menu


# Status Bar

text_size = 11
statusBar = Label(root, text="Size  :  " + str(text_size) + "    |    ANSI    |    Line : 1 | Col : 1 ", anchor=E, bd=1,
                  relief=SUNKEN)

statusBar.pack(side=BOTTOM, fill=X)


# Scrollbar

hscroll = Scrollbar(root, orient=HORIZONTAL, repeatdelay=100000)
vscroll = Scrollbar(root, orient=VERTICAL, troughcolor='red', bg='orange')
hscroll.pack(side=BOTTOM, fill=X, anchor=SE)
vscroll.pack(side=RIGHT, fill=Y, anchor=NE)

# Text style

tst = Font(family="Lucida Console", size=text_size)

# Text

editor = Text(root, font=tst, wrap=NONE, undo=TRUE, xscrollcommand=hscroll.set, yscrollcommand=vscroll.set)

editor.bind("<Button-3>", popup)  # Popup Menu Binding
editor.bind("<Control-s>", save)
editor.bind("<Control-n>", new)
editor.bind("<Control-o>", opens)
editor.bind("<Control-g>", search)
editor.bind("<Control-t>", counts)
editor.bind("<Control-d>", time_date)
editor.bind("<Tab>", tab)
editor.bind("<Control-b>", build_run)

root.bind("<Key>", update_status_bar)
root.bind("<Button>", update_status_bar)
root.bind("<Enter>", update_status_bar)
root.bind("<Leave>", update_status_bar)

editor.focus_set()  # To select text box at open

editor.pack(expand=TRUE, fill=BOTH, side=LEFT)

hscroll.config(command=editor.xview)
vscroll.config(command=editor.yview)
hscroll['width'] = 0

# Menu

m = Menu(root)
root.config(menu=m)

fm = Menu(m, tearoff=0)
m.add_cascade(label="File", menu=fm)
fm.add_command(label="New                    ", command=new, accelerator="Ctrl+N")
fm.add_command(label="Open", command=opens, accelerator="Ctrl+O")
fm.add_separator()
fm.add_command(label="Save", command=save, accelerator="Ctrl+S")
fm.add_command(label="Save As", command=save_as)
fm.add_separator()
fm.add_command(label="Exit", command=root.quit)

em = Menu(m, tearoff=0)
m.add_cascade(label="Edit", menu=em)
em.add_command(label="Cut                    ", command=cut, accelerator="Ctrl+X")
em.add_command(label="Copy", command=copy, accelerator="Ctrl+C")
em.add_command(label="Paste", command=paste, accelerator="Ctrl+P")
em.add_separator()
em.add_command(label="Undo", command=editor.edit_undo, accelerator="Ctrl+Z")
em.add_command(label="Redo", command=editor.edit_redo, accelerator="Ctrl+Y")
em.add_separator()
em.add_command(label="Select All", command=select_all, accelerator="Ctrl+A")

sm = Menu(m, tearoff=0)
m.add_cascade(label="Special", menu=sm)
sm.add_command(label="Count                  ", command=counts, accelerator="Ctrl+T")
sm.add_command(label="Search", command=search, accelerator="Ctrl+G")
sm.add_command(label="Time/Date", command=time_date, accelerator="Ctrl+D")

setm = Menu(m, tearoff=0)
m.add_cascade(label="Settings", menu=setm)
setm.add_command(label="Text Size            ", command=adjust_text_size)
setm.add_command(label="Text Type", command=adjust_text_type)
setm.add_command(label="Text Style", command=adjust_text_style)
wrap = IntVar()
setm.add_checkbutton(label="Word Wrap", variable=wrap, command=adjust_wrap)
status = IntVar()
setm.add_checkbutton(label="Status Bar", variable=status, command=set_status)
status.set(1)

thm = Menu(m, tearoff=0)
m.add_cascade(label="Themes", menu=thm)
dark = StringVar()
dark.set("Default")
thm.add_radiobutton(label="Default", variable=dark, command=themes)
thm.add_radiobutton(label="Dark Theme", variable=dark, command=themes)
thm.add_radiobutton(label="Great Green", variable=dark, command=themes)
thm.add_radiobutton(label="Violet", variable=dark, command=themes)

bm = Menu(m, tearoff=0)
m.add_cascade(label="Build", menu=bm)
bm.add_command(label="Build And Run", command=build_run, accelerator="Ctrl+B")

hm = Menu(m, tearoff=0)
m.add_cascade(label="Help", menu=hm)
hm.add_command(label="About Us", command=helps)

# Popup Menu

popup_menu = Menu(root, tearoff=0)

popup_menu.add_command(label="Cut", command=cut)
popup_menu.add_command(label="Copy", command=copy)
popup_menu.add_command(label="Paste", command=paste)
popup_menu.add_separator()
popup_menu.add_command(label="Undo", command=editor.edit_undo)
popup_menu.add_command(label="Redo", command=editor.edit_redo)
popup_menu.add_separator()
popup_menu.add_command(label="Select All\t\t\t", command=select_all)
popup_menu.add_separator()
popup_menu.add_command(label="Build And Run", command=build_run)

root.protocol("WM_DELETE_WINDOW", close)
root.mainloop()
