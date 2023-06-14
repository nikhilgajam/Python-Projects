import tkinter
import os
import urllib.request as req
import random
import threading


PATH = "store.data"
joke_list = []


def getNewJoke():
    try:
        data = str(req.urlopen("https://v2.jokeapi.dev/joke/Programming?format=txt").read(), "ascii", "ignore")
        return data
    except Exception:
        return "Error"


def writeOperation(data: str):
    if data not in joke_list:
        wp = open(PATH, "a")
        wp.write(data)
        wp.close()


def readOperation():
    global joke_list

    rp = open(PATH, "r")
    data = rp.read()
    rp.close()

    joke_list = data.split(" |#| ")


def loadJoke():
    global joke_list

    displayData("Loading A New Joke...")

    joke = getNewJoke()

    if joke != "Error":
        writeOperation(joke + " |#| ")
        displayData(joke)

    if joke == "Error" and os.path.exists(PATH):
        readOperation()
        displayData(random.choice(joke_list))
        return
    elif joke == "Error" and not os.path.exists(PATH):
        displayData("You need to have internet for the first time to load jokes.")
        return


def newJokeBtnClicked(e=""):
    threading.Thread(target=loadJoke).start()


def displayData(data: str):
    display['state'] = tkinter.NORMAL
    display.delete("1.0", tkinter.END)
    display.insert(tkinter.INSERT, data)
    display['state'] = tkinter.DISABLED


window = tkinter.Tk()
window.title("Joke Teller")

heading = tkinter.Label(window, text="Joke Teller", font=("Stencil", 28))
heading.pack()

display = tkinter.Text(window, font=("Times New Roman", 15), cursor="arrow", height=15, wrap="word")
display.pack(fill=tkinter.BOTH, expand=tkinter.TRUE)

new_joke_btn = tkinter.Button(window, text="New Joke", font=("Stencil", 15), command=newJokeBtnClicked)
new_joke_btn.pack()

newJokeBtnClicked()
window.mainloop()
