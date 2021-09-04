from tkinter import *
import wikipedia
import threading
import urllib.request as req
from tkinter import messagebox
import time

root = Tk()
root.title("Today In History")
root.config(background="black")
root.iconbitmap(True, "images/icon.ico")


def joke_load():
    try:
        display.config(cursor="watch")
        display.config(state=DISABLED)

        joke = str(req.urlopen("https://v2.jokeapi.dev/joke/Any?format=txt").read(), "utf-8")
        display.config(state=NORMAL)
        display.insert(INSERT, "Joke:\n\n", "data_tag")
        display.insert(INSERT, joke + "\n\n\n")  # https://sv443.net/jokeapi/v2/
        display.config(state=DISABLED)
    except Exception:
        messagebox.showerror("Error", "Check Your Internet Connection")


def wiki_load():
    try:
        date = time.strftime("%d %b")
        wiki_data = wikipedia.page(date).content
        display.config(state=NORMAL)
        display.insert(INSERT, "Information:\n\n", "data_tag")
        display.insert(INSERT, wiki_data.replace(".\n", ".\n\n").replace("===\n", "===\n\n"))

        display.config(cursor="arrow")
        display.config(state=DISABLED)

    except wikipedia.exceptions.PageError:
        date = time.strftime("%d %B")
        wiki_data = wikipedia.page(date).content
        display.config(state=NORMAL)
        display.insert(INSERT, "Information:\n\n", "data_tag")
        display.insert(INSERT, wiki_data.replace(".\n", ".\n\n").replace("===\n", "===\n\n"))

        display.config(cursor="arrow")
        display.config(state=DISABLED)
        display.insert(INSERT, "Check Your Internet Connection.")

    except Exception:
        display.insert(INSERT, "Check Your Internet Connection.")


# Scroll Bar
scroll_bar = Scrollbar(root)
scroll_bar.pack(side=RIGHT, fill=Y)

# Display
display = Text(root, fg="#fd910b", bg="#000000", font=("Lucida Console", 13), wrap="word",
               yscrollcommand=scroll_bar.set)
display.pack(expand=TRUE, fill=BOTH, padx=1, pady=1)
display.tag_config("data_tag", foreground="#dadce0")

scroll_bar.config(command=display.yview)
display.insert(INSERT, time.strftime("%A %B %d, %Y\n\n"))

# Loading the content using threading
threading.Thread(target=joke_load, args=()).start()
threading.Thread(target=wiki_load, args=()).start()

root.mainloop()
