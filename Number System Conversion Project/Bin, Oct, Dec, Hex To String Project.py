from tkinter import *
from tkinter import messagebox

root = Tk()
root.geometry("750x590")
root.iconbitmap(True, "images/icon.ico")
root.title("Bin, Oct, Hex To String")


def process(event=""):
    convert = str(ent.get(0.0, END)).rstrip()

    lis = convert.split()

    string = ""

    try:

        if num.get() == 1:
            for i in lis:
                string += chr(int(i, 2))   # Base 2 is binary
        elif num.get() == 2:
            for i in lis:
                string += chr(int(i, 8))   # Base 8 is octal
        elif num.get() == 3:
            for i in lis:
                string += chr(int(i, 10))  # Base 10 is decimal
        elif num.get() == 4:
            for i in lis:
                string += chr(int(i, 16))  # Base 16 is hexadecimal

        display.delete(0.0, END)
        display.insert(END, string.rstrip())

    except ValueError:
        display.delete(0.0, END)
        messagebox.showerror("Error", "Select Correct Type Of Number System")


def copies_to_clipboard():
    ent.clipboard_clear()
    ent.clipboard_append(display.get(1.0, END))


def clipboard_paste():
    ent.delete(1.0, END)
    ent.insert(INSERT, str(ent.clipboard_get()))


# Heading


lbl = Label(root, font="Pristina 40", text="Bin, Oct, Hex To String")
lbl.pack()

# Entry

ent = Text(root, fg="#dadce0", bg="#35363a", font="Verdana 16", wrap="word", insertbackground="#dadce0", height=7)
ent.focus()
ent.bind("<Return>", process)
ent.pack(expand=TRUE, fill=BOTH)

# Paste Button

pst_btn = Button(root, text="Clipboard Paste", fg="white", bg="gray", command=clipboard_paste)
pst_btn.pack()

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

btn = Button(root, text="Process", fg="white", bg="black", command=process)
btn.pack()

# Output Display Text

display = Text(root, fg="#dadce0", bg="#35363a", font="Verdana 12", wrap="word", insertbackground="#dadce0", height=11)
display.pack(expand=TRUE, fill=BOTH)

# Copy Button

cpy_btn = Button(root, text="Copy Answer", fg="white", bg="gray", command=copies_to_clipboard)
cpy_btn.pack()

root.mainloop()
