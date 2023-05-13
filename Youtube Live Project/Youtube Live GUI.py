from YoutubeLiveAPI import YoutubeLive
from tkinter import *
from tkinter import messagebox
import threading
import webbrowser


# Window settings
window = Tk()
window.title("Youtube Live")
window.geometry("800x500")

# Variables
data = {}

# Methods

def search():
    global data
    inp = search_box.get()
    
    list_box.delete(0, END)
    list_box.insert(0, "Searching In Youtube")
    list_box.insert(1, "Wait For A Moment")

    data = YoutubeLive().getList(inp)

    if data == "Check Your Internet Connection":
        messagebox.showerror("Error", "Check Your Internet Connection")
        return

    list_box.delete(0, END)
    for i, j in enumerate(data.keys()):
        list_box.insert(i, str(j))

    list_box.focus()
    list_box.select_set(0)


def searchUsingThread(e=""):
    threading.Thread(target=search).start()


def open(e=""):
    selected = list_box.get(ACTIVE)
    if selected != "Searching In Youtube" or selected != "Wait For A Moment":
        webbrowser.open(data[selected])


# Heading label
heading = Label(window, text="Youtube Live", font=("Times New Roman", 26))
heading.pack(fill=BOTH, expand=TRUE)

# Listbox and its scrollbar
scroll_bar = Scrollbar(window, orient="vertical", bg="#333333", troughcolor="#333333")
scroll_bar.pack(side=RIGHT, fill=Y, anchor=NE)

list_box = Listbox(window, fg="#e6e8eb", bg="#333333", yscrollcommand=scroll_bar.set,
                    font=("Times New Roman", 15), selectbackground="#993e1c")
list_box.bind("<Return>", open)
scroll_bar.config(command=list_box.yview)
list_box.pack(fill=BOTH, expand=TRUE)

# Open button
open_btn = Button(window, text="Open Selected Stream", command=open)
open_btn.pack(pady=10)

# Search box
search_box = Entry(window, font=("Times New Roman", 15))
search_box.bind("<Return>", searchUsingThread)
search_box.focus()
search_box.pack(fill=X, expand=TRUE, padx=10, pady=10)

# Search button
search_btn = Button(window, text="Search", command=searchUsingThread)
search_btn.pack(pady=10)


window.mainloop()
