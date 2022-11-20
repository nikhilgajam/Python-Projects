from tkinter import *
from tkinter import messagebox
import SongLyricsAPI


# SongLyricsAPI Object
SongAPI = SongLyricsAPI.SongLyrics()

# Global Variables
artists = ""
switch = True
song_name = ""
artist_name = ""


# Commands

def clickToGoToSearchBox(e=""):
    search_box.focus_force()


def methodSwitch(e=""):
    if switch == True:
        artistSearch()
    else:
        getSong()

def artistSearch():
    global artists, switch, song_name, artist_name

    song_name = search_box.get()

    if song_name == None or song_name == "":
        messagebox.showwarning("Warning", "Enter a song name")
    else:
        artists = SongAPI.getArtists(song_name)

        if artists[0] == "Entered song is unavailable":
            messagebox.showwarning("Warning", "Entered song is not valid or not available")
            return

        display.config(state=NORMAL)
        display.delete(1.0, END)
        display.insert(1.0, "Enter Any One Artist Name Which Is Shown Below:\n\n")
        for i in artists:
            display.insert(INSERT, i + "\n")
        display.config(state=DISABLED)

        search_box.delete(0, END)
        search_btn["text"] = "Get Lyrics"

        switch = not switch


def getSong():
    global switch

    artist_name = search_box.get()
    if artist_name not in artists:
        messagebox.showwarning("Warning", "Enter an artist name shown on the screen")
    else:
        lyrics = SongAPI.getLyrics(artist_name)
        display.config(state=NORMAL)
        display.delete(1.0, END)

        song_title = artist_name + " " + song_name + " Lyrics:\n"
        song_title = song_title.title()

        display.insert(INSERT, song_title)
        display.insert(INSERT, "=" * (len(song_title)-2) + "\n\n")

        display.insert(INSERT, lyrics)
        display.config(state=DISABLED)

        switch = not switch
        search_btn["text"] = "Get Artist Names"
        search_box.delete(0, END)
        

# Window
window = Tk()
window.title("GetLyrics")

# Display
display = Text(window, wrap="word")
display.pack(expand=TRUE, fill=BOTH, padx=10, pady=10)
display.insert("1.0", "Instructions:\n\nEnter song name in the search box")
display.bind("<Button-1>", clickToGoToSearchBox)
display.bind("<Button-3>", clickToGoToSearchBox)
display.configure(state=DISABLED)

# Search Box
search_box = Entry(window)
search_box.pack(expand=TRUE, fill=BOTH, padx=6, pady=10)
search_box.bind("<Return>", methodSwitch)
search_box.focus()

# Button
search_btn = Button(window, text="Get Artist Names", command=methodSwitch)
search_btn.pack(padx=10, pady=4)


window.mainloop()
