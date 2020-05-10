import os
import time
import threading
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from ttkthemes import themed_tk as tk
from pygame import mixer
from mutagen.mp3 import MP3
import tkinter.messagebox


root = tk.ThemedTk()
root.get_themes()
root.set_theme('black')
root.iconbitmap(True, "images\\n.ico")
root.title("Nikhil Music")
root.resizable(0, 0)
# root.geometry("300x300")
mixer.init()

# Status Bar

statusBar = ttk.Label(root, text="Welcome To Nikhil Music")
statusBar.pack(side=BOTTOM, fill=X)


# Commands used

pathName = TRUE
paused = FALSE
muted = FALSE
playlist = []


def play():
    global paused
    global pathName

    if paused:
        mixer.music.unpause()
        statusBar['text'] = 'Music Resumed'
        paused = FALSE
    else:
        try:
            sel_song = plb1.curselection()
            sel_song = int(sel_song[0])
            play_it = playlist[sel_song]
            mixer.music.load(play_it)
            mixer.music.play()
            pathName = play_it
            statusBar['text'] = 'Playing Music:' + ' ' + os.path.basename(pathName)
            details(play_it)
        except:
            tkinter.messagebox.showerror("Song", "Select a song by clicking Player > Open \nAlso you can click Add Button\nAnd Select A Song")


def stop():
    mixer.music.stop()  # Music stopping statement
    statusBar['text'] = "Music Stopped"


def rewind():
    mixer.music.play()
    statusBar['text'] = 'Music Rewinded' + ' ' + os.path.basename(pathName)


def pause():
    global paused
    paused = TRUE
    mixer.music.pause()
    statusBar['text'] = 'Music Paused:' + ' ' + os.path.basename(pathName)


def mute():
    global muted
    if muted:
        b5.configure(image=mutePic)
        scale.set(0.5)
        mixer.music.set_volume(0.5)
        muted = FALSE
        statusBar['text'] = 'Music Unmuted:'
    else:
        mixer.music.set_volume(0)
        scale.set(0)
        b5.configure(image=volPic)
        muted = TRUE
        statusBar['text'] = 'Music Muted:'


def vol(val):
    volume = float(val)   # Volume adjustment
    mixer.music.set_volume(volume)


def about():
    tkinter.messagebox.showinfo("About Us", "Nikhil Music")  # Prompt information


def ask():
    asks = tkinter.messagebox.askquestion("Exit", "Do You Want To Exit")  # Prompt to close

    if asks == "yes":
        root.destroy()  # To quit the window
    else:
        pass


def open_file():
    global pathName
    pathName = filedialog.askopenfilename()  # Opening a open window
    play_list_box(pathName)


def details(pathName):
    nameLabel['text'] = os.path.basename(pathName)
    tag = os.path.splitext(pathName)
    if tag[1] == '.mp3':
        mp = MP3(pathName)
        tl = mp.info.length

    else:
        wa = mixer.Sound(pathName)
        tl = wa.get_length()

    minu, seco = divmod(tl, 60)
    minu = round(minu)
    seco = round(seco)
    ml = '{:02d}:{:02d}'.format(minu, seco)
    lengthLabel['text'] = 'Music Length = ' + ml

    t1 = threading.Thread(target=count, args=(tl,))
    t1.start()


def count(t):
    global paused
    counts = 0
    while counts <= t and mixer.music.get_busy():
        if paused:
            continue
        else:
            minu, seco = divmod(counts, 60)
            minu = round(minu)
            seco = round(seco)
            ml = '{:02d}:{:02d}'.format(minu, seco)
            currentLenLabel['text'] = 'Music Length = ' + ml
            time.sleep(1)
            counts += 1


def close_button():
    stop()
    root.destroy()


def play_list_box(names):
    names = os.path.basename(names)
    index = 0
    plb1.insert(index, names)
    playlist.insert(index, pathName)
    index += 1


def del_song():
    sel_song = plb1.curselection()
    sel_song = int(sel_song[0])
    plb1.delete(sel_song)
    playlist.pop(sel_song)

# Menu


m = Menu(root)
root.config(menu=m)

cm = Menu(m, tearoff=0)
m.add_cascade(label="Player", menu=cm)
cm.add_command(label="Open", command=open_file)
cm.add_separator()
cm.add_command(label="Exit", command=ask)

am = Menu(m, tearoff=0)
m.add_cascade(label="About", menu=am)
am.add_command(label="About Us", command=about)

left = ttk.Frame(root)
left.pack(side=LEFT, padx=7)

right = ttk.Frame(root)
right.pack(side=RIGHT, padx=7)

# Listbox

plb1 = Listbox(left, fg="white", bg="gray")
plb1.pack(side=TOP)
b1 = ttk.Button(left, text="+ ADD", command=open_file)
b1.pack(side=LEFT, padx=3)
b2 = ttk.Button(left, text="- DEL", command=del_song)
b2.pack(side=LEFT, padx=3)

# Label

nameLabel = ttk.Label(right, text="Nikhil Music")
nameLabel.pack()

lengthLabel = ttk.Label(right, text="Music Length = --:--")
lengthLabel.pack()

currentLenLabel = ttk.Label(right, text="Current Length = --:--", relief=GROOVE)
currentLenLabel.pack()

# Buttons with pictures

middle = ttk.Frame(right)
middle.pack(padx=3, pady=3)

playPic = PhotoImage(file=r"images\play.png")
b1 = ttk.Button(middle, image=playPic, command=play)
b1.grid(row=0, column=0, padx=3, pady=3)

pausePic = PhotoImage(file=r"images\pause.png")
b2 = ttk.Button(middle, image=pausePic, command=pause)
b2.grid(row=0, column=1, padx=3, pady=3)

stopPic = PhotoImage(file=r"images\stop.png")
b3 = ttk.Button(middle, image=stopPic, command=stop)
b3.grid(row=0, column=2, padx=3, pady=3)

bottom = ttk.Frame(right)
bottom.pack()

rewindPic = PhotoImage(file=r"images\rewind.png")
b4 = ttk.Button(bottom, image=rewindPic, command=rewind)
b4.grid(row=0, column=0)

mutePic = PhotoImage(file=r"images\mute.png")
volPic = PhotoImage(file=r"images\volume.png")
b5 = ttk.Button(bottom, image=mutePic, command=mute)
b5.grid(row=0, column=2)

# Volume Slider

scale = ttk.Scale(bottom, orient=HORIZONTAL, command=vol)
scale.set(0.5)
mixer.music.set_volume(0.5)
scale.grid(row=0, column=1, padx=3, pady=11)

root.protocol("WM_DELETE_WINDOW", close_button)
root.mainloop()
