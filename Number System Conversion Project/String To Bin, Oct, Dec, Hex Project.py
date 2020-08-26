from tkinter import *

root = Tk()
root.iconbitmap(True, "images/icon.ico")
root.title("String To Bin, Oct, Dec, Hex")


def process(event=""):
    convert = str(ent.get()).rstrip()

    lis = []

    if num.get() == 1:
        for i in convert:
            lis.append(str('0') + bin(ord(i))[2:])
    elif num.get() == 2:
        for i in convert:
            lis.append(oct(ord(i))[2:])
    elif num.get() == 3:
        for i in convert:
            lis.append(ord(i))
    elif num.get() == 4:
        for i in convert:
            lis.append(hex(ord(i))[2:])

    string = ""

    for i in lis:
        string += str(i) + str(" ")

    display.delete(0.0, END)
    display.insert(END, string.rstrip())

# Heading


lbl = Label(root, font="Pristina 40", text="String To Bin, Oct, Dec, Hex")
lbl.pack()

# Entry

ent = Entry(root, font="Verdana 16")
ent.focus()
ent.bind("<Return>", process)
ent.pack(expand=TRUE, fill=BOTH)

# Radio Buttons

num = IntVar()

rb_container = Frame(root)
rb_container.pack()

rb1 = Radiobutton(rb_container, text="Binary", variable=num, value=1, command=process)
rb1.select()
rb1.pack(side=LEFT)
rb2 = Radiobutton(rb_container, text="Octal", variable=num, value=2, command=process)
rb2.pack(side=LEFT)
rb3 = Radiobutton(rb_container, text="Decimal", variable=num, value=3, command=process)
rb3.pack(side=LEFT)
rb4 = Radiobutton(rb_container, text="Hexadecimal", variable=num, value=4, command=process)
rb4.pack(side=LEFT)

# Empty Line

space = Label(root)
space.pack()

# Process Button

btn = Button(root, text="Process", fg="white", bg="gray", command=process)
btn.pack()

# Output Display Text

display = Text(root, fg="#dadce0", bg="#35363a", font="Verdana 12", wrap="word", insertbackground="#dadce0")
display.pack(expand=TRUE, fill=BOTH)

root.mainloop()
