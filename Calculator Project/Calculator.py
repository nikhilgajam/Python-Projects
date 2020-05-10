from tkinter import *
import tkinter.messagebox

root = Tk()
root.geometry("250x400+300+300")
# root.resizable(0, 0)
root.title("Nikhil's Calculator")
root.iconbitmap(True, "icons\calc.ico")

# Button on press

val = ""
store = 0
operator = ""


def btn1_clicked():
    global val
    val = val + '1'
    data.set(val)    # data StringVar() is created in Label section


def btn2_clicked():
    global val
    val = val + '2'
    data.set(val)


def btn3_clicked():
    global val
    val = val + '3'
    data.set(val)


def btn4_clicked():
    global val
    val = val + '4'
    data.set(val)


def btn5_clicked():
    global val
    val = val + '5'
    data.set(val)


def btn6_clicked():
    global val
    val = val + '6'
    data.set(val)


def btn7_clicked():
    global val
    val = val + '7'
    data.set(val)


def btn8_clicked():
    global val
    val = val + '8'
    data.set(val)


def btn9_clicked():
    global val
    val = val + '9'
    data.set(val)


def btn0_clicked():
    global val
    val = val + '0'
    data.set(val)


def btnp_clicked():
    global val
    global store
    global operator
    store = int(val)
    operator = '+'
    val = val + '+'
    data.set(val)


def btnm_clicked():
    global val
    global store
    global operator
    store = int(val)
    operator = '-'
    val = val + '-'
    data.set(val)


def btnml_clicked():
    global val
    global store
    global operator
    store = int(val)
    operator = '*'
    val = val + '*'
    data.set(val)


def btnd_clicked():
    global val
    global store
    global operator
    store = int(val)
    operator = '/'
    val = val + '/'
    data.set(val)


def btnc_clicked():
    global val
    global store
    global operator
    val = ""
    store = 0
    operator = ""
    data.set(val)


def btneq_clicked():
    global val
    global store
    global operator
    temp = val

    if operator == '+':
        val2 = int((temp.split('+')[1]))
        ans = store + val2
        data.set(ans)
        val = str(ans)

    elif operator == '-':
        val2 = int((temp.split('-')[1]))
        ans = store - val2
        data.set(ans)
        val = str(ans)

    elif operator == '*':
        val2 = int((temp.split('*')[1]))
        ans = store * val2
        data.set(ans)
        val = str(ans)

    elif operator == '/':
        val2 = int((temp.split('/')[1]))

        if val2 == 0:
            tkinter.messagebox.showerror("Error: Division By Zero", "Division By Zero Goes To Infinity")
            val = ""
            store = 0
            operator = ""
            data.set(val)
        else:
            ans = store / val2
            data.set(ans)
            val = str(ans)


# Label

data = StringVar()

label = Label(root, anchor=SE, font="Verdana 20", textvariable=data, fg="black", bg="gray")
label.pack(expand=TRUE, fill=BOTH)

# Row 1 Buttons

btnrow1 = Frame(root, bg="#000000")
btnrow1.pack(expand=TRUE, fill=BOTH)

btn1 = Button(btnrow1, text="1", font="Segoe 23", relief=GROOVE, bd=0, command=btn1_clicked, fg="white", bg="#333333")
btn1.pack(side=LEFT, expand=TRUE, fill=BOTH)

btn2 = Button(btnrow1, text="2", font="Segoe 23", relief=GROOVE, bd=0,  command=btn2_clicked, fg="white", bg="#333333")
btn2.pack(side=LEFT, expand=TRUE, fill=BOTH)

btn3 = Button(btnrow1, text="3", font="Segoe 23", relief=GROOVE, bd=0, command=btn3_clicked, fg="white", bg="#333333")
btn3.pack(side=LEFT, expand=TRUE, fill=BOTH)

btnp = Button(btnrow1, text="+", font="Segoe 23", relief=GROOVE, bd=0, command=btnp_clicked, fg="white", bg="#333333")
btnp.pack(side=LEFT, expand=TRUE, fill=BOTH)

# Row 2 Buttons

btnrow2 = Frame(root)
btnrow2.pack(expand=TRUE, fill=BOTH)

btn4 = Button(btnrow2, text="4", font="Segoe 23", relief=GROOVE, bd=0, command=btn4_clicked, fg="white", bg="#333333")
btn4.pack(side=LEFT, expand=TRUE, fill=BOTH)

btn5 = Button(btnrow2, text="5", font="Segoe 23", relief=GROOVE, bd=0, command=btn5_clicked, fg="white", bg="#333333")
btn5.pack(side=LEFT, expand=TRUE, fill=BOTH)

btn6 = Button(btnrow2, text="6", font="Segoe 23", relief=GROOVE, bd=0, command=btn6_clicked, fg="white", bg="#333333")
btn6.pack(side=LEFT, expand=TRUE, fill=BOTH)

btnm = Button(btnrow2, text="-", font="Segoe 23", relief=GROOVE, bd=0, command=btnm_clicked, fg="white", bg="#333333")
btnm.pack(side=LEFT, expand=TRUE, fill=BOTH)

# Row 3 Buttons

btnrow3 = Frame(root)
btnrow3.pack(expand=TRUE, fill=BOTH)

btn7 = Button(btnrow3, text="7", font="Segoe 23", relief=GROOVE, bd=0, command=btn7_clicked, fg="white", bg="#333333")
btn7.pack(side=LEFT, expand=TRUE, fill=BOTH)

btn8 = Button(btnrow3, text="8", font="Segoe 23", relief=GROOVE, bd=0, command=btn8_clicked, fg="white", bg="#333333")
btn8.pack(side=LEFT, expand=TRUE, fill=BOTH)

btn9 = Button(btnrow3, text="9", font="Segoe 23", relief=GROOVE, bd=0, command=btn9_clicked, fg="white", bg="#333333")
btn9.pack(side=LEFT, expand=TRUE, fill=BOTH)

btnml = Button(btnrow3, text="*", font="Segoe 23", relief=GROOVE, bd=0, command=btnml_clicked, fg="white", bg="#333333")
btnml.pack(side=LEFT, expand=TRUE, fill=BOTH)

# Row 4 Buttons

btnrow4 = Frame(root)
btnrow4.pack(expand=TRUE, fill=BOTH)

btnc = Button(btnrow4, text="C", font="Segoe 23", relief=GROOVE, bd=0, command=btnc_clicked, fg="white", bg="#333333")
btnc.pack(side=LEFT, expand=TRUE, fill=BOTH)

btn0 = Button(btnrow4, text="0", font="Segoe 23", relief=GROOVE, bd=0, command=btn0_clicked, fg="white", bg="#333333")
btn0.pack(side=LEFT, expand=TRUE, fill=BOTH)

btneq = Button(btnrow4, text="=", font="Segoe 23", relief=GROOVE, bd=0, command=btneq_clicked, fg="white", bg="#333333")
btneq.pack(side=LEFT, expand=TRUE, fill=BOTH)

btnd = Button(btnrow4, text="/", font="Segoe 23", relief=GROOVE, bd=0, command=btnd_clicked, fg="white", bg="#333333")
btnd.pack(side=LEFT, expand=TRUE, fill=BOTH)


root.mainloop()
