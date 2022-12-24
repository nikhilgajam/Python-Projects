from tkinter import *
import subprocess
import os

# Variables
chp_ver_nos = {0:0, 1:47, 2:72, 3:43, 4:42, 5:29, 6:47, 7:30, 8:28, 9:34, 10:42, 11:55, 12:20, 13:35, 14:27, 15:20, 16:24, 17:28, 18:78}

chapter_list = []
verse_list = ['', ]
language_list = ['English', 'Hindi', 'Telugu']

path = ""

for i in chp_ver_nos.keys():
        chapter_list.append("Chapter " + str(i))

chapter_selected = 0
verse_selected = 0
language_selected = 'English'


# Methods
def controlsInit():
    global verse_list

    verse_list = []

    for i in range(chp_ver_nos[chapter_selected]+1):
        verse_list.append("Verse " + str(i))

    verse_menu = OptionMenu(control_area, verse_var, *verse_list, command=controlSelect)
    verse_menu.grid(row=0, column=3, padx=6, pady=4)

    chapter_var.set("Chapter " + str(chapter_selected))
    verse_var.set("Verse " + str(verse_selected))
    language_var.set(language_selected)


def chapterControlSelect(e=""):
    global chapter_selected, verse_selected, language_selected

    chapter_selected = int(chapter_var.get().split(' ')[1])
    verse_selected = 0
    language_selected = language_var.get()

    os.system('"Data/Pictures/Chapter ' + str(chapter_selected) + '.jpg"')

    controlsInit()
    loadData()


def controlSelect(e=""):
    global chapter_selected, verse_selected, language_selected

    chapter_selected = int(chapter_var.get().split(' ')[1])
    verse_selected = int(verse_var.get().split(' ')[1])
    language_selected = language_var.get()

    loadData()


def loadData():
    global path

    if language_selected == "English":
        path = "Data/Bhagavad_Gita/English/"
    elif language_selected == "Hindi":
        path = "Data/Bhagavad_Gita/Hindi/"
    elif language_selected == "Telugu":
        path = "Data/Bhagavad_Gita/Telugu/"

    path = path + "Chapter_" + str(chapter_selected) + "/Verse_" + str(verse_selected) + ".txt"

    p = open(path, "r", encoding='utf-8')
    data = p.read()
    p.close()

    display.config(state=NORMAL)
    display.delete(1.0, END)
    display.insert(INSERT, data)
    display.config(state=DISABLED)


def prevChapterClicked(e=""):
    global chapter_selected,  verse_selected

    if chapter_selected - 1 >= 0:
        chapter_selected -= 1
        verse_selected = 0
        chapter_var.set("Chapter " + str(chapter_selected))
        controlsInit()
        loadData()
        os.system('"Data/Pictures/Chapter ' + str(chapter_selected) + '.jpg"')


def nextChapterClicked(e=""):
    global chapter_selected, verse_selected

    if chapter_selected + 1 <= 18:
        chapter_selected += 1
        verse_selected = 0
        chapter_var.set("Chapter " + str(chapter_selected))
        controlsInit()
        loadData()
        os.system('"Data/Pictures/Chapter ' + str(chapter_selected) + '.jpg"')


def prevVerseClicked(e=""):
    global chapter_selected,  verse_selected

    if verse_selected - 1 >= 0:
        verse_selected -= 1
        verse_var.set("Verse " + str(verse_selected))
        loadData()
    elif chapter_selected - 1 >= 0:
        chapter_selected -= 1
        verse_selected = chp_ver_nos[chapter_selected]
        chapter_var.set("Chapter " + str(chapter_selected))
        controlsInit()
        loadData()



def nextVerseClicked(e=""):
    global chapter_selected,  verse_selected

    if verse_selected + 1 <= chp_ver_nos[chapter_selected]:
        verse_selected += 1
        verse_var.set("Verse " + str(verse_selected))
        loadData()
    elif chapter_selected + 1 <= 18:
        chapter_selected += 1
        verse_selected = 0
        chapter_var.set("Chapter " + str(chapter_selected))
        controlsInit()
        loadData()


# Window settings
window = Tk()
window.title("The Bhagavad Gita")
window.config(bg="#333333")

# Title
title = Label(window, text="The Bhagavad Gita", font=("Times New Roman", 26), fg="#e6e8eb", bg="#333333")
title.pack()

# Partitions
area = Frame(window, bg="#333333")
area.pack()

# Display
display = Text(window, wrap="word", font=("Times New Roman", 16), fg="#e6e8eb", bg="#333333", cursor="arrow")
display.pack(expand=TRUE, fill=BOTH)

# Contols
control_area = Frame(window, bg="#333333")
control_area.pack()

chapter_var = StringVar()
chapter_menu = OptionMenu(control_area, chapter_var, *chapter_list, command=chapterControlSelect)
chapter_menu.grid(row=0, column=2, padx=6, pady=4)

verse_var = StringVar()
verse_menu = OptionMenu(control_area, verse_var, *verse_list, command=controlSelect)
verse_menu.grid(row=0, column=3, padx=6, pady=4)

language_var = StringVar()
language_menu = OptionMenu(control_area, language_var, *language_list, command=controlSelect)
language_menu.grid(row=0, column=4, padx=6, pady=4)

# Buttons

prev_chapter = Button(control_area, text="<<", command=prevChapterClicked)
prev_chapter.grid(row=0, column=0, padx=6, pady=4)

prev_verse = Button(control_area, text="<", command=prevVerseClicked)
prev_verse.grid(row=0, column=1, padx=6, pady=4)

next_verse = Button(control_area, text=">", command=nextVerseClicked)
next_verse.grid(row=0, column=5, padx=6, pady=4)

next_chapter = Button(control_area, text=">>", command=nextChapterClicked)
next_chapter.grid(row=0, column=6, padx=6, pady=4)

# Initial method calls
controlsInit()
loadData()

window.mainloop()
