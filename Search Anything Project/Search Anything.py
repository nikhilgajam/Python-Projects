from tkinter import *
from tkinter import messagebox as tm
from tkinter import filedialog
from tkinter import ttk
import webbrowser
import wikipedia
import threading
import time

root = Tk()
root.geometry("942x542")
root.title("Search Anything")
root.iconbitmap(True, "images/icon.ico")
root.resizable(0, 0)

# Commands


def search():

    def save_as(event=""):
        path = filedialog.asksaveasfilename(initialfile="Search Anything.txt", defaultextension=".txt", filetype=(("Text Document", "*.txt"), ("All Files", "*.*")))
        with open(path, "w", encoding="utf8") as p:
            p.write(str(data))

    def popup(event):
        popup_menu.post(event.x_root, event.y_root)    # Popup menu

    def cut():
        copy()
        text.delete("sel.first", "sel.last")

    def copy():
        text.clipboard_clear()
        text.clipboard_append(text.selection_get())

    def paste():
        text.insert(INSERT, text.clipboard_get())

    def select_all():
        text.tag_add(SEL, "1.0", END)
        text.mark_set(INSERT, 1.0)
        text.see(INSERT)

    def randoms(event="", ch=1):
        text.config(cursor="exchange")
        e1.delete(0, END)
        e1.insert(0, random_name)
        new_thread()

    def about():
        webbrowser.open("https://youtube.com/nikhiltech")
        tm.showinfo("About Us", "This Code Is Written By Nikhil")

    sear = Toplevel()
    sear.title("Data")
    sear.geometry("752x457")
    sear.config(cursor="watch")

    # Scrollbar

    scroll = ttk.Scrollbar(sear)
    scroll.pack(side=RIGHT, fill=Y)

    # Text Box

    text = Text(sear, wrap="word", yscrollcommand=scroll.set, fg="#e6e8eb", bg="#2c4079", font=20, undo=TRUE, spacing1=12, insertbackground="white")
    text.bind("<Button-3>", popup)
    text.bind("<Control-r>", randoms)
    text.bind("<Control-s>", save_as)
    text.focus_set()
    text.pack(expand=TRUE, fill=BOTH, side=LEFT)
    text.config(cursor="watch")

    scroll.config(command=text.yview)

    # Menu

    mm = Menu(sear)
    sear.config(menu=mm)

    amm = Menu(mm, tearoff=0)
    mm.add_cascade(label="Save", menu=amm)
    amm.add_command(label="Save As            Ctrl+S", command=save_as)

    emm = Menu(mm, tearoff=0)
    mm.add_cascade(label="Edit", menu=emm)
    emm.add_command(label="Cut               Ctrl+X", command=cut)
    emm.add_command(label="Copy            Ctrl+C", command=copy)
    emm.add_command(label="Paste            Ctrl+V", command=paste)
    emm.add_separator()
    emm.add_command(label="Undo            Ctrl+Z", command=text.edit_undo)
    emm.add_command(label="Redo             Ctrl+Y", command=text.edit_redo)

    rmm = Menu(mm, tearoff=0)
    mm.add_cascade(label="Random", menu=rmm)
    rmm.add_command(label="Open Random Suggestion             Ctrl+R", command=randoms)

    asmm = Menu(mm, tearoff=0)
    mm.add_cascade(label="About Us", menu=asmm)
    asmm.add_command(label="About Creator", command=about)

    # Popup Menu

    popup_menu = Menu(root, tearoff=0)

    popup_menu.add_command(label="Open Random Suggestion", command=randoms)
    popup_menu.add_separator()
    popup_menu.add_command(label="Save As", command=save_as)
    popup_menu.add_separator()
    popup_menu.add_command(label="Cut", command=cut)
    popup_menu.add_command(label="Copy", command=copy)
    popup_menu.add_command(label="Paste", command=paste)
    popup_menu.add_separator()
    popup_menu.add_command(label="Undo", command=text.edit_undo)
    popup_menu.add_command(label="Redo", command=text.edit_redo)
    popup_menu.add_separator()
    popup_menu.add_command(label="Select All\t\t\t", command=select_all)

    # Time And Date

    time_date = time.strftime("%I:%M:%S %p  %A - %d/%B/%Y")

    dp.config(cursor="watch")
    e1.config(cursor="watch")
    b1.config(cursor="watch")

    try:

        ask = e1.get()

        if ask == "Type Anything Here":
            data = "You Can Type Anything In This Box And Get Answers\nClear The Words Which Are Entered In Type Anything Box By Using Backspace Key\nCheck Your Internet Connection Because Without Internet This Program Will Not Work"
        elif ask == "Nikhil Tech":
            data = "Nikhil Tech is a youtube channel created by Nikhil\nYou can go to that channel by clicking About Us and then About Creator\nAlso you can type https://www.youtube.com/NikhilTech to go to Nikhil Tech Youtube Channel"
        else:
            data = wikipedia.page(ask).content

        # Random Wikipedia Suggestion

        if ask == "Type Anything Here":
            random_name = "Nikhil Tech"
        else:
            random_name = wikipedia.random()

        sear.deiconify()

        # Data insertion

        text.delete(1.0, END)
        text.insert(END, time_date)
        if ask == "Type Anything Here":
            pass
        else:
            text.insert(END, "\nRandom Suggestion :  " + random_name)
        text.insert(END, "\n\n")
        if ask == "Type Anything Here":
            text.insert(END, ">>>  " + ask + "  <<<\n\n" + data)
        elif ask == "Nikhil Tech":
            text.insert(END, ">>>  " + ask + "  <<<\n\n" + data)
        else:
            text.insert(END, ">>>  " + wikipedia.page(ask).title + "  <<<\n\n" + data)

        sear.config(cursor="arrow")
        text.config(cursor="arrow")
        root.config(cursor="arrow")
        dp.config(cursor="arrow")
        e1.config(cursor="arrow")
        b1.config(cursor="arrow")

    except:
        sear.destroy()
        tm.showerror("Problem", "Check Your Keyword And Internet Connection")
        root.config(cursor="arrow")
        dp.config(cursor="arrow")
        e1.config(cursor="arrow")
        b1.config(cursor="arrow")


def new_thread(event=""):
    x = threading.Thread(target=search, args=())
    x.start()


def about_us():
    webbrowser.open("https://youtube.com/nikhiltech")
    tm.showinfo("About Us", "This Code Is Written By Nikhil")


# Image

pic = PhotoImage(file="images/pic.png")
dp = Label(root, image=pic)
dp.pack()

# Menu

m = Menu(root)
root.config(menu=m)

am = Menu(m, tearoff=0)
m.add_cascade(label="About", menu=am)
am.add_command(label="About Us", command=about_us)

# Label

lbl = Label(root, text="Search Anything", font=20, fg="white", bg="#04043c")
lbl.bind("<Return>", search)
lbl.place(x=410, y=3)

# Entry

e1 = Entry(root, width=40, font="Verdana 19", fg="#e6e8eb", bg="#2c4079", bd=0, insertbackground="#e6e8eb")
e1.insert(0, "Type Anything Here")
e1.bind("<Return>", new_thread)
e1.focus_set()
e1.place(x=141, y=200)

# Button

b1 = Button(root, text="Search", fg="#e6e8eb", bg="#2c4079", command=new_thread)
b1.place(x=451, y=250)

root.mainloop()
