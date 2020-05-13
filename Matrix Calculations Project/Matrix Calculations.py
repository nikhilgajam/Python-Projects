from tkinter import *
from tkinter import ttk
from tkinter import messagebox as tm
import numpy as np


root = Tk()
root.title("Matrix Calculations")
root.geometry("883x652")
root.iconbitmap(True, 'images\\icon.ico')  # Smooth Icon Management
root.resizable(0, 0)

data = StringVar()
count = 0

label = Label(root, textvariable=data, font="Pristina 25")
label.pack(expand=TRUE, fill=BOTH)
data.set("Matrix Calculations")

# Commands


def add():
    try:
        r1 = int(er1.get())
        c1 = int(ec1.get())
        r2 = int(er2.get())
        c2 = int(ec2.get())

        data.set("Matrix Addition")
        arr = []
        arr = (e1.get())
        arr = arr.split(" ")
        k = 0
        for i in arr:
            arr[k] = float(i)
            k += 1

        arr = np.array([arr])

        arr1 = []
        arr1 = (e2.get())
        arr1 = arr1.split(" ")

        k = 0
        for j in arr1:
            arr1[k] = float(j)
            k += 1

        arr1 = np.array([arr1])
        ans = 0

        try:
            arr = np.reshape(arr, (r1, c1))
            arr1 = np.reshape(arr1, (r2, c2))
            ans = arr+arr1

            text.delete(1.0, END)
            text.insert(END, "Entered Matrix 1:\n" + str(arr)+"\n"+"Entered Matrix 2:" + "\n" + str(arr1))
            text.insert(END, "\n\nAnswer:\n"+str(ans))

        except ValueError:
            text.delete(1.0, END)
            tm.showerror("Dimensional Error", "Check The Entered Values")

    except ValueError:
        text.delete(1.0, END)
        tm.showerror("Value Error", "Enter Valid Input(Only Numbers)")


def sub():
    try:
        r1 = int(er1.get())
        c1 = int(ec1.get())
        r2 = int(er2.get())
        c2 = int(ec2.get())

        data.set("Matrix Subtraction")
        arr = []
        arr = (e1.get())
        arr = arr.split(" ")
        k = 0
        for i in arr:
            arr[k] = float(i)
            k += 1

        arr = np.array([arr])     # dtype = int64 and more

        arr1 = []
        arr1 = (e2.get())
        arr1 = arr1.split(" ")

        k = 0
        for j in arr1:
            arr1[k] = float(j)
            k += 1

        arr1 = np.array([arr1])
        ans = 0

        try:
            arr = np.reshape(arr, (r1, c1))
            arr1 = np.reshape(arr1, (r2, c2))
            ans = arr-arr1

            text.delete(1.0, END)
            text.insert(END, "Entered Matrix 1:\n" + str(arr)+"\n" + "Entered Matrix 2:" + "\n" + str(arr1))
            text.insert(END, "\n\nAnswer:\n"+str(ans))

        except ValueError:
            text.delete(1.0, END)
            tm.showerror("Dimensional Error", "Check The Entered Values")

    except ValueError:
        text.delete(1.0, END)
        tm.showerror("Value Error", "Enter Valid Input(Only Numbers & Decimals)")


def mult():
    try:
        r1 = int(er1.get())
        c1 = int(ec1.get())
        r2 = int(er2.get())
        c2 = int(ec2.get())

        data.set("Matrix Multiplication")
        arr = []
        arr = (e1.get())
        arr = arr.split(" ")
        k = 0
        for i in arr:
            arr[k] = float(i)
            k += 1

        arr = np.array([arr])

        arr1 = []
        arr1 = (e2.get())
        arr1 = arr1.split(" ")

        k = 0
        for j in arr1:
            arr1[k] = float(j)
            k += 1

        arr1 = np.array([arr1])
        ans = 0

        try:
            arr = np.reshape(arr, (r1, c1))
            arr1 = np.reshape(arr1, (r2, c2))
            ans = arr.dot(arr1)

            text.delete(1.0, END)
            text.insert(END, "Entered Matrix 1:\n" + str(arr)+"\n" + "Entered Matrix 2:" + "\n" + str(arr1))
            text.insert(END, "\n\nAnswer:\n"+str(ans))

        except ValueError:
            text.delete(1.0, END)
            tm.showerror("Dimensional Error", "Check The Entered Values")

    except ValueError:
        text.delete(1.0, END)
        tm.showerror("Value Error", "Enter Valid Input(Only Numbers & Decimals)")


def div():
    try:
        r1 = int(er1.get())
        c1 = int(ec1.get())
        r2 = int(er2.get())
        c2 = int(ec2.get())

        data.set("Matrix Division")
        arr = []
        arr = (e1.get())
        arr = arr.split(" ")
        k = 0
        for i in arr:
            arr[k] = float(i)
            k += 1

        arr = np.array([arr])

        arr1 = []
        arr1 = (e2.get())
        arr1 = arr1.split(" ")

        k = 0
        for j in arr1:
            arr1[k] = float(j)
            k += 1

        arr1 = np.array([arr1])
        ans = 0

        try:
            arr = np.reshape(arr, (r1, c1))
            arr1 = np.reshape(arr1, (r2, c2))
            ans = arr/arr1

            text.delete(1.0, END)
            text.insert(END, "Entered Matrix 1:\n" + str(arr) + "\n" + "Entered Matrix 2:" + "\n" + str(arr1))
            text.insert(END, "\n\nAnswer:\n"+str(ans))

        except ValueError:
            text.delete(1.0, END)
            tm.showerror("Dimensional Error", "Check The Entered Values")

    except ValueError:
        text.delete(1.0, END)
        tm.showerror("Value Error", "Enter Valid Input(Only Numbers & Decimals)")


def tran():
    try:
        r1 = int(er1.get())
        c1 = int(ec1.get())

        data.set("Matrix Transpose")
        arr = []
        arr = (e1.get())
        arr = arr.split(" ")
        k = 0
        for i in arr:
            arr[k] = float(i)
            k += 1

        arr = np.array([arr])

        try:
            arr = np.reshape(arr, (r1, c1))
            ans = np.transpose(arr)

            text.delete(1.0, END)
            text.insert(END, "Entered Matrix 1:\n" + str(arr))
            text.insert(END, "\n\nAnswer:\n" + str(ans))

        except ValueError:
            text.delete(1.0, END)
            tm.showerror("Dimensional Error", "Check The Entered Values")

    except ValueError:
        text.delete(1.0, END)
        tm.showerror("Value Error", "Enter Valid Input(Only Numbers & Decimals)")


def det():
    try:
        r1 = int(er1.get())
        c1 = int(ec1.get())

        data.set("Matrix Determinant")
        arr = []
        arr = (e1.get())
        arr = arr.split(" ")
        k = 0
        for i in arr:
            arr[k] = float(i)
            k += 1

        arr = np.array([arr])

        try:
            arr = np.reshape(arr, (r1, c1))
            ans = round(np.linalg.det(arr))

            text.delete(1.0, END)
            text.insert(END, "Entered Matrix 1:\n" + str(arr))
            text.insert(END, "\n\nAnswer:\n" + str(ans))

        except:
            text.delete(1.0, END)
            tm.showerror("Dimensional Error", "Check The Entered Values")

    except ValueError:
        text.delete(1.0, END)
        tm.showerror("Value Error", "Enter Valid Input(Only Numbers & Decimals)")


def inv():
    try:
        r1 = int(er1.get())
        c1 = int(ec1.get())

        data.set("Matrix Inverse")
        arr = []
        arr = (e1.get())
        arr = arr.split(" ")
        k = 0
        for i in arr:
            arr[k] = float(i)
            k += 1

        arr = np.array([arr])

        try:
            arr = np.reshape(arr, (r1, c1))
            ans = np.linalg.inv(arr)

            text.delete(1.0, END)
            text.insert(END, "Entered Matrix 1:\n" + str(arr))
            text.insert(END, "\n\nAnswer:\n" + str(ans))

        except:
            text.delete(1.0, END)
            tm.showerror("Dimensional Error", "Check The Entered Values")

    except:
        text.delete(1.0, END)
        tm.showerror("Value Error", "Enter Valid Input(Only Numbers & Decimals)")


def about_us():
    tm.showinfo("About Us", "This Code Is Written By Nikhil")


def helps():
    text.delete(1.0, END)
    text.insert(END, "1.Enter the matrix in linear form in the Enter Matrix 1 & 2 Values Section\n")
    text.insert(END, "2.Press Space Bar After Each Value(Give No Space Before & After You Entering The Values)\n")
    text.insert(END, "3.You can enter 'N' no. of values in the same Matrix 1 & 2 Values Section (OR) Box\n")
    text.insert(END, "4.You can Scroll the Answer Box by using Scroll Wheel or UP & DOWN Arrows\n")
    text.insert(END, "5.You can quickly write something in the Answer Box\n")
    text.insert(END, "6.You can Select text in Answer Box by pressing CTRL+A(OR)Drag With Mouse(OR)Press SHIFT+ARROWS\n")
    text.insert(END, "7.You can Copy the values by pressing CTRL+C keys\n")

    text.insert(END, "\n\n\n\t\t\t\tThanks for using\n")


# Menu

m = Menu(root)
root.config(menu=m)

am = Menu(m, tearoff=0)
m.add_cascade(label="About", menu=am)
am.add_command(label="About Us", command=about_us)
am.add_command(label="Help", command=helps)


# Top
top = Frame(root)
top.pack(expand=TRUE, fill=BOTH)

la1 = ttk.Label(top, text="Matrix 1 :")
la1.grid(row=0, column=1, padx=3, pady=3)
lr1 = ttk.Label(top, text="      Rows : ")
lr1.grid(row=1, column=0, padx=3, pady=3)
er1 = ttk.Entry(top, width=60)
er1.grid(row=1, column=1, padx=3, pady=3)
lc1 = ttk.Label(top, text="Columns : ")
lc1.grid(row=2, column=0, padx=3, pady=3)
ec1 = ttk.Entry(top, width=60)
ec1.grid(row=2, column=1, padx=3, pady=3)

la2 = ttk.Label(top, text="Matrix 2 :")
la2.grid(row=0, column=3, padx=3, pady=3)
lr2 = ttk.Label(top, text="      Rows : ")
lr2.grid(row=1, column=2, padx=3, pady=3)
er2 = ttk.Entry(top, width=60)
er2.grid(row=1, column=3, padx=3, pady=3)
lc2 = Label(top, text="Columns : ")
lc2.grid(row=2, column=2, padx=3, pady=3)
ec2 = ttk.Entry(top, width=60)
ec2.grid(row=2, column=3, padx=3, pady=3)

# Middle
middle = Frame(root)
middle.pack(expand=TRUE, fill=BOTH)

lbl0 = Label(middle, text="________________________________________________________________________________________________________________________________________________________________________")
lbl0.pack()
lbl = Label(middle, text="Enter Values By Giving Space Between Each Value", font="Verdana 12")
lbl.pack()

left = Frame(middle)
left.pack(side=LEFT)

l1 = ttk.Label(left, text="Enter Matrix 1 Values : ")
l1.pack(padx=3, pady=3)
e1 = ttk.Entry(left, width=70)
e1.pack(padx=6, pady=6)

right = Frame(middle)
right.pack(side=RIGHT)

l2 = ttk.Label(right, text="Enter Matrix 2 Values : ")
l2.pack(padx=3, pady=3)
e2 = ttk.Entry(right, width=70)
e2.pack(padx=6, pady=6)

# Bottom
top = Frame(root)
top.pack(expand=TRUE, fill=BOTH)

b1 = ttk.Button(top, text="Addition", command=add)
b1.pack(side=LEFT, expand=TRUE, fill=BOTH)
b2 = ttk.Button(top, text="Subtraction", command=sub)
b2.pack(side=LEFT, expand=TRUE, fill=BOTH)
b3 = ttk.Button(top, text="Multiplication", command=mult)
b3.pack(side=LEFT, expand=TRUE, fill=BOTH)
b4 = ttk.Button(top, text="Division", command=div)
b4.pack(side=LEFT, expand=TRUE, fill=BOTH)
b5 = ttk.Button(top, text="Transpose", command=tran)
b5.pack(side=LEFT, expand=TRUE, fill=BOTH)
b6 = ttk.Button(top, text="Determinant", command=det)
b6.pack(side=LEFT, expand=TRUE, fill=BOTH)
b7 = ttk.Button(top, text="Inverse", command=inv)
b7.pack(side=LEFT, expand=TRUE, fill=BOTH)

# Answer
answer = Frame(root)
answer.pack(side=BOTTOM)

text = Text(answer, height=15, font="Calibri 16", fg="white", bg="#2b3d40")
text.pack()

root.mainloop()
