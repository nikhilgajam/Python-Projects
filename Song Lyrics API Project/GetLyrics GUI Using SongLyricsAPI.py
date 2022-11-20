from tkinter import *
from tkinter import messagebox
import SongLyricsAPI


# SongLyricsAPI Object
SongAPI = SongLyricsAPI.SongLyrics()

# Global Variables
artists = ""
switch = True
no_of_songs = 0

# ASCII Art
book_ascii_art = '''
\t\t\t     ,         ,
\t\t\t     |\\\\\\\\ ////|
\t\t\t     | \\\\\\V/// |
\t\t\t     |  |~~~|  |
\t\t\t     |  |===|  |
\t\t\t     |  |Lyr|  |
\t\t\t     |  |ics|  |
\t\t\t      \ |   | /
\t\t\t       \|===|/
\t\t\t        '---'
'''

hourglass_ascii_art = """
        ____....----''''````    |.
,'''````            ____....----; '.
| __....----''''````         .-.`'. '.
|.-.                .....    | |   '. '.
`| |        ..:::::::::::::::| |   .-;. |
 | |`'-;-::::::::::::::::::::| |,,.| |-='
 | |   | ::::::::::::::::::::| |   | |
 | |   | :::::::::::::::;;;;;| |   | |
 | |   | :::::::::;;;()()()()| |   | |
 | |   | :::::;;()()()()()()(| |   | |
 | |   | :::;()()()()()()()()| |   | |
 | |   | :;()()()()()()()(+++| |   | |
 | |   | |;()()()()()++++++++| |   | |
 | |   | | ;++++++++++++++++;| |   | |
 | |   | |  ;++++++++++++++;.| |   | |
 | |   | |   :++++++++++++:  | |   | |
 | |   | |    .:++++++++;.   | |   | |
 | |   | |       .:;+:..     | |   | |
 | |   | |         ;;        | |   | |
 | |   | |      .,:+;:,.     | |   | |
 | |   | |    .::::;+::::,   | |   | |
 | |   | |   ::::::;;::::::. | |   | |
 | |   | |  :::::::+;:::::::.| |   | |
 | |   | | ::::::::;;::::::::| |   | |
 | |   | |:::::::::+:::::::::| |   | |
 | |   | |:::::::::+:::::::::| |   | |
 | |   | ::::::::;+++;:::::::| |   | |
 | |   | :::::::;+++++;::::::| |   | |
 | |   | ::::::;+++++++;:::::| |   | |
 | |   |.:::::;+++++++++;::::| |   | |
 | | ,`':::::;+++++++++++;:::| |'"-| |-..
 | |'   ::::;+++++++++++++;::| |   '-' ,|
 | |    ::::;++++++++++++++;:| |     .' |
,;-'_   `-._===++++++++++_.-'| |   .'  .'
|    ````'''----....___-'    '-' .'  .'
'---....____           ````'''--;  ,'
            ````''''----....____|.'
"""


# Commands

def clickToGoToSearchBox(e=""):
    search_box.focus_force()


def methodSwitch(e=""):
    if switch == True:
        artistSearch()
    else:
        getSong()

def artistSearch():
    global artists, switch, no_of_songs

    song_name = search_box.get()

    if song_name == None or song_name == "":
        messagebox.showwarning("Warning", "Enter a song name")
    else:
        artists = SongAPI.getArtists(song_name)
        no_of_songs = len(artists)

        if artists[0] == "Entered song is unavailable":
            messagebox.showwarning("Warning", "Entered song is not available or not valid")
            return

        display.config(state=NORMAL)
        display.delete(1.0, END)
        display.insert(1.0, "Enter Song Number Of Any Given Song In The Search Box:\n")
        display.insert(INSERT, " "*4 + " [___________]\n") 
        display.insert(INSERT, " "*11 + "|\n" + " "*11 + "|\n" + " "*11 + "|\n  ." + "_"*8 +"|\n  |\n  V\n\n") 

        c = 1
        for i in artists:
            display.insert(INSERT,  "[ " + str(c) + " ] " + i + "\n")
            c += 1

        display.insert(INSERT, "\n\nIf You Cannot Find The Wanted Song In The Given List Then Click On That " + 
                               "Home Button And Try Typing Artist Name With Song Name.")

        display.insert(INSERT, "\n\n" + hourglass_ascii_art)
        
        display.config(state=DISABLED)

        search_box.delete(0, END)
        search_btn["text"] = "  Get Lyrics  "

        switch = not switch


def getSong():
    global switch

    artist_number = search_box.get()
    if not artist_number.isdigit():
        messagebox.showwarning("Warning", "Enter correct [ song number ] shown on the screen")
        return

    artist_number = int(artist_number)

    if artist_number < 1 or artist_number > no_of_songs:  # Checking whether entered number is invalid or not 
        messagebox.showwarning("Warning", "Enter valid [ song number ] shown on the screen")
    else:
        lyrics = SongAPI.getLyrics(artists[artist_number-1])
        display.config(state=NORMAL)
        display.delete(1.0, END)

        song_title = artists[artist_number-1] + ":\n"
        song_title = song_title.title()

        display.insert(INSERT, song_title)
        display.insert(INSERT, "~" * (len(song_title)-2) + "\n\n")

        display.insert(INSERT, lyrics + "\n\n\n" + hourglass_ascii_art)
        display.config(state=DISABLED)

        switch = not switch
        search_btn["text"] = "Song Search"
        search_box.delete(0, END)


def home(e=""):
    global switch
    switch = True
    search_btn["text"] = "Song Search"

    display.config(state=NORMAL)
    display.delete(1.0, END)
    display.insert("1.0", "Instructions:\n" + "~"*13 + "\n\nEnter Song Name In The Search Box.\n\nThis Program Needs Internet.\n\n")
    display.insert(INSERT, book_ascii_art.rstrip())
    display.config(state=DISABLED)
    search_box.focus()
        

# Window
window = Tk()
window.geometry("942x542")
window.configure(bg="#7c7e87")
window.title("GetLyrics")

# Display
display = Text(window, wrap="word", font=("Lucida Console", 16), fg="#e6e8eb", bg="#333333", cursor="arrow")
display.pack(expand=TRUE, fill=BOTH, padx=10, pady=4)
display.bind("<Button-1>", clickToGoToSearchBox)
display.bind("<Button-3>", clickToGoToSearchBox)
display.configure(state=DISABLED)

# Scrollbar
scroll = Scrollbar(display, orient="vertical", command=display.yview)
scroll.pack(side=RIGHT, fill=Y)
display.configure(yscrollcommand=scroll.set)
scroll.config(command=display.yview)

searchArea = Frame(window)
searchArea.pack(pady=10)

# Home Button
home_btn = Button(searchArea, text="Home (⌂)", command=home)
home_btn.grid(row=0, column=0, padx=10, pady=4)

# Search Box
search_box = Entry(searchArea, font=("Lucida Console", 14), width=60, fg="#e6e8eb", bg="#333333", insertbackground="#e6e8eb")
search_box.grid(row=0, column=1, padx=6, pady=10)
search_box.bind("<Return>", methodSwitch)
search_box.focus()

# Search Button
search_btn = Button(searchArea, text="Song Search", command=methodSwitch)
search_btn.grid(row=0, column=2, padx=10, pady=4)

# Displays Home Page
home()

window.mainloop()
