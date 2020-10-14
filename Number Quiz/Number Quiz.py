from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import playsound
import threading
import random

root = Tk()
root.iconbitmap(True, "images/icon.ico")
root.title("Number Quiz")

symbols = ['+', '-', '*', '/', '%', '^']
c = m = ans = num1 = num2 = sym = 0

# Commands


def evaluate(event=""):
    global c, m, ans, num1, num2, sym

    ent.focus()

    try:
        num1 = random.randint(0, int(range_num.get()))
        num2 = random.randint(1, int(range_num.get()))

        sym = random.choice(symbols)

        question['text'] = str(num1) + " " + sym + " " + str(num2) + " = "

        if sym == '+':
            ans = num1 + num2

        elif sym == '-':
            ans = num1 - num2

        elif sym == '*':
            ans = num1 * num2

        elif sym == '/':
            ans = num1 / num2
            ans = "%.2f" % ans
            if float(ans) == int(float(ans)):
                ans = int(float(ans))

        elif sym == '%':
            ans = num1 % num2

        elif sym == '^':
            if int(range_num.get()) < 10:
                x = int(range_num.get())
            else:
                x = 9
            num1 = random.randint(1, x)
            num2 = random.randint(1, x)
            question['text'] = str(num1) + " " + sym + " " + str(num2) + " = "
            ans = num1 ** num2

    except Exception as ex:
        messagebox.showerror("Error", "Enter Numbers")


def answer(event=""):
    global c, m, sym

    if str(ans) == ent.get():
        c += 1
        score['text'] = "Correct : " + str(c) + " \t\t Mistake : " + str(m) + "\n"
        # playsound.playsound("sounds/correct.mp3")
        t = threading.Thread(target=sounds, args=(1,))
        t.start()
    else:
        m += 1
        score['text'] = "Correct : " + str(c) + " \t\t Mistake : " + str(m) + "\n"
        # playsound.playsound("sounds/mistake.mp3")
        t = threading.Thread(target=sounds, args=(0,))
        t.start()

    ans_lbl['text'] = "\n" + str(num1) + " " + str(sym) + " " + str(num2) + " = " + str(ans)
    ent.delete(0, END)
    # Displaying New Question
    evaluate()


def sounds(x):
    if x == 1:
        playsound.playsound("sounds/correct.mp3")
    else:
        playsound.playsound("sounds/mistake.mp3")


def helps():
    top = Toplevel()
    top.title("Help")
    top.attributes("-toolwindow", 1)
    top.focus_set()
    
    help_lbl = Label(top, font="Pristina 40", text="Number Quiz\nVersion: 1\nDeveloped By: Nikhil \n\nHelp: ", justify=LEFT)
    help_lbl.pack()

    lbl = Label(top, font="Verdana 8", text="To Check Type The Answer In The Answer Box And Hit Enter Or Press Check Button\nTo Change The Range Select Range Box And Type The Range And Hit Enter Key\n\nThanks for using....")
    lbl.pack()

    about_button = ttk.Button(top, text="OK", state=ACTIVE, command=top.destroy)
    about_button.pack(padx=6, pady=6)

    top.mainloop()


# Heading

lbl = Label(root, font="Pristina 60", text="Number Quiz")
lbl.pack()

# Menu

menu = Menu(root)
root.config(menu=menu)

help_menu = Menu(menu, tearoff=0)
menu.add_cascade(label="Help", menu=help_menu)
help_menu.add_cascade(label="Help", command=helps)

# Score

score = Label(root, font="16", text="Correct : 0 \t\t Mistake : 0\n")
score.pack()

# Question

q = Frame(root)
q.pack()

question = Label(q, font="Rockwell 40")
question.grid(row=1, column=0)

# Answer Box

ent = Entry(q, font="Rockwell 40", width=8)
ent.focus()
ent.bind("<Return>", answer)
ent.grid(row=1, column=2)

# Previous answer

ans_lbl = Label(root, font="Arial 17", text="\nStart Answering")
ans_lbl.pack()

# Check Button

btn = ttk.Button(root, text="Check", command=answer, width=10)
btn.pack()

# Space

space = Label(root)
space.pack()

# Range (Press Enter To Change The Range)

range_area = Frame(root)
range_area.pack()

range_lbl = Label(range_area, text="Range : ")
range_lbl.grid(row=3, column=0)

range_num = Entry(range_area, width=6)
range_num.insert(0, "100")
range_num.bind("<Return>", evaluate)
range_num.grid(row=3, column=3)

evaluate()

root.mainloop()
