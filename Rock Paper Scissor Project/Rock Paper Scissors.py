from tkinter import *
from tkinter import ttk
from tkinter.font import Font
from playsound import playsound
import webbrowser
import random

user_points = 0
comp_points = 0
count = 0
items = ["Rock", "Paper", "Scissors"]
c_sound = u_sound = t_sound = 0

# Commands


def game(get):
    global user_points, comp_points, count, c_sound, u_sound, t_sound, text
    screen['state'] = NORMAL

    if count == 0:
        screen.delete(1.0, END)


    count += 1

    user = get

    entered = ""

    if 'r' in user:
        entered = "Rock"
    elif 'p' in user:
        entered = "Paper"
    elif 's' in user:
        entered = "Scissors"

    screen.insert(END, "(" + str(count) + ")" + "  User : " + str(entered) + '\n')

    comp = random.choice(items)

    screen.insert(END, "Computer : " + str(comp) + '\n')

    if comp == entered:
        screen.insert(END, ">>> Tie" + "\n")
        t_sound = 1
    elif comp == "Rock" and entered == "Paper":
        screen.insert(END, ">>> You Got A Point: Paper Covered The Rock" + "\n")
        user_points += 1
        u_sound = 1
    elif comp == "Paper" and entered == "Rock":
        screen.insert(END, ">>> Computer Got A Point: Paper Covered The Rock" + "\n")
        comp_points += 1
        c_sound = 1
    elif comp == "Scissors" and entered == "Rock":
        screen.insert(END, ">>> You Got A Point: Rock Smashed The Scissors" + "\n")
        user_points += 1
        u_sound = 1
    elif comp == "Rock" and entered == "Scissors":
        screen.insert(END, ">>> Computer Got A Point: Rock Smashed The Scissors" + "\n")
        comp_points += 1
        c_sound = 1
    elif comp == "Paper" and entered == "Scissors":
        screen.insert(END, ">>> You Got A Point: Scissors Cuts The Paper" + "\n")
        user_points += 1
        u_sound = 1
    elif comp == "Scissors" and entered == "Paper":
        screen.insert(END, ">>> Computer Got A Point: Scissors Cuts The Paper" + "\n")
        comp_points += 1
        c_sound = 1

    if sound_var.get() == "on":
        if u_sound == 1:
            playsound("sounds/You_point.mp3")
        elif c_sound == 1:
            playsound("sounds/Computer_point.mp3")
        elif t_sound == 1:
            playsound("sounds/Tie.mp3")

    c_sound = u_sound = t_sound = 0

    screen.insert(END, "\n")
    screen.yview(END)  # Auto Scroll
    score_lbl['text'] = "Player : " + str(user_points) + " \t\t Computer : " + str(comp_points)
    screen['state'] = DISABLED
    screen.focus_set()


def rock(event=""):
    game('r')


def paper(event=""):
    game('p')


def scissor(event=""):
    game('s')


def radio_command(event=""):
    screen.focus_set()


def about(event=""):
    top = Toplevel()
    top.title("About")
    top.attributes("-toolwindow", 1)
    top.focus_set()

    about_lbl = Label(top, font="Mistral 40", text="Rock Paper Scissors\n\nVersion: 1\nDeveloped By: Nikhil", justify=LEFT)
    about_lbl.pack()

    about_button = ttk.Button(top, text="OK", state=ACTIVE, command=top.destroy)
    about_button.pack(padx=6, pady=6)

    tell()

    top.mainloop()

def tell():
    playsound("sounds/about.mp3")
    webbrowser.open("https://www.youtube.com/NikhilTech")


def done(event=""):
    global user_points, comp_points, count

    screen['state'] = NORMAL
    screen.insert(END, "\n")
    if user_points > comp_points:
        screen.insert(END, "\n\nYou Won" + "\nYou Got : " + str(user_points) + " Point(s)" + "\nComputer Got : " +
                      str(comp_points) + " Point(s)" + "\n\n\n")
    elif user_points == comp_points:
        screen.insert(END, "\n\nTie" + "\nYou Got : " + str(user_points) + " Point(s)" + "\nComputer Got : " +
                      str(comp_points) + " Point(s)" + "\n\n\n")
    else:
        screen.insert(END, "\n\nComputer Won" + "\nYou Got : " + str(user_points) + " Point(s)" + "\nComputer Got : " +
                      str(comp_points) + " Point(s)" + "\n\n\n")

    if sound_var.get() == "on":
        if user_points > comp_points:
            playsound("sounds/You_won.mp3")
        elif comp_points > user_points:
            playsound("sounds/Computer_won.mp3")
        else:
            playsound("sounds/Tie.mp3")

    screen.yview(END)  # Auto Scroll
    screen['state'] = DISABLED
    screen.focus_set()
    user_points = comp_points = 0
    score_lbl['text'] = "Player : " + str(user_points) + " \t\t Computer : " + str(comp_points)


# Main


root = Tk()
root.title("Rock Paper Scissors")
root.iconbitmap(True, "images/icon.ico")

# Menu

menu = Menu(root)
root.config(menu=menu)

about_menu = Menu(menu, tearoff=0)
menu.add_cascade(label="About", menu=about_menu)
about_menu.add_command(label="About Creator", command=about)

# Header

header = Frame(root)
header.pack()

lbl = Label(header, text="Rock Paper Scissors", font="Pristina 46")
lbl.pack()

# Score

score = Frame(root)
score.pack()

score_lbl = Label(score, text="Player : 0 \t\t Computer : 0")
score_lbl.pack()

# Screen


text_display = "Welcome To Rock Paper Scissors Game\n\nYou Can Press 1 2 3 Keys On Keyboard To Represent Rock Paper " \
               "Scissors\nAnd You Can Click Rock Paper Scissors Buttons Or Keys To Start\nYou Can Turn Sounds " \
               "On & Off BySelecting On & Off Radio Buttons\nPress Enter Or Click Done To Get The Score And Reset " \
               " The Game\n\n\t\t               Let's Get Started..."

text = Font(family="Pristina", size=21)

screen = Text(root, fg="white", bg="#2b3d40", font=text, wrap="word", height=12, width=60, cursor="arrow")
screen.focus_set()
screen.pack()

screen.insert(END, text_display)
screen.configure(state=DISABLED)

screen.bind("<Key-1>", rock)
screen.bind("<Key-2>", paper)
screen.bind("<Key-3>", scissor)
screen.bind("<Return>", done)

# Rock Paper Scissor Buttons

buttons = Frame(root)

buttons.pack()

btn1 = ttk.Button(buttons, text="Rock", command=rock)
btn1.grid(row=0, column=0, padx=6)

btn2 = ttk.Button(buttons, text="Paper", command=paper)
btn2.grid(row=0, column=1, padx=6)

btn3 = ttk.Button(buttons, text="Scissor", command=scissor)
btn3.grid(row=0, column=2, padx=6)

# Radio Buttons

radio = Frame(root, border=1)
radio.pack()

sound_var = StringVar()
s_lbl = ttk.Label(radio, text="Sounds")
s_lbl.grid(row=0, column=2)

sounds_on = ttk.Radiobutton(radio, variable=sound_var, value="on", text="On", command=radio_command)
sounds_on.invoke()
sounds_on.grid(row=1, column=0)

sounds_mute = ttk.Radiobutton(radio, variable=sound_var, value="off", text="Off", command=radio_command)
sounds_mute.grid(row=1, column=3)

# Done Button

done = ttk.Button(root, text="Done", command=done).pack(padx=5, pady=3)

root.mainloop()
