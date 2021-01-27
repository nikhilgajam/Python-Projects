from tkinter import *
from tkinter import ttk
from tkinter import messagebox as tm
import numpy as np


root = Tk()
root.title("Matrix Calculations")
root.geometry("883x652")
root.iconbitmap(True, 'images\\icon.ico')  # Smooth Icon Management
root.resizable(0, 0)

# data Stores the heading text
data = StringVar()

# mat1&2_data stores array values
mat1_data = ""
mat2_data = ""

# Heading
label = Label(root, textvariable=data, font="Pristina 25")
label.pack(expand=TRUE, fill=BOTH)
data.set("Matrix Calculations")

# Commands


def get_data(num):
    try:
        # Row and column data
        # if the num value is 1 then it indicates both rows and columns need to be entered else one row and one column is enough

        if num == 1:
            r1 = int(er1.get().strip())
            c1 = int(ec1.get().strip())
            r2 = int(er2.get().strip())
            c2 = int(ec2.get().strip())
        else:
            r1 = int(er1.get().strip())
            c1 = int(ec1.get().strip())
            r2 = 0
            c2 = 0

        # Changing the text data to list by splitting

        arr = str(mat1_data).strip().replace("\n", " ")
        arr = arr.split(" ")

        if num == 1:
            arr1 = str(mat2_data).strip().replace("\n", " ")
            arr1 = arr1.split(" ")
        else:
            arr1 = 0

        # Changing the list data to float data type
        for i, k in enumerate(arr):
            arr[i] = float(k)

        if num == 1:
            for i, k in enumerate(arr1):
                arr1[i] = float(k)

        # Converting the list to Numpy array
        arr = np.array([arr])   # We can add dtype = int64 and more
        arr1 = np.array([arr1])

        try:
            # Changing the linear array to the array that we entered in row and column boxes
            arr = np.reshape(arr, (r1, c1))
            if num == 1:
                arr1 = np.reshape(arr1, (r2, c2))

            return arr, arr1

        except ValueError:
            text.delete(1.0, END)
            tm.showerror("Dimensional Error", "Check The Entered Values")
            # When exception is triggered then it return None values
            return None, None

    except ValueError:
        text.delete(1.0, END)
        tm.showerror("Value Error", "Enter Valid Input(Only Numbers)\nAnd Don't Leave Row And Column Boxes Blank")
        # When exception is triggered then it return None values
        return None, None


def add():
    data.set("Matrix Addition")

    arr, arr1 = get_data(1)
    if arr is None or arr1 is None:
        return

    # Array addition
    ans = arr + arr1

    text.delete(1.0, END)
    text.insert(END, "Entered Matrix 1:\n" + str(arr)+"\n"+"Entered Matrix 2:" + "\n" + str(arr1))
    text.insert(END, "\n\nAnswer:\n"+str(ans))


def sub():
    data.set("Matrix Subtraction")

    arr, arr1 = get_data(1)
    if arr is None or arr1 is None:
        return

    # Array subtraction
    ans = arr - arr1

    text.delete(1.0, END)
    text.insert(END, "Entered Matrix 1:\n" + str(arr)+"\n" + "Entered Matrix 2:" + "\n" + str(arr1))
    text.insert(END, "\n\nAnswer:\n"+str(ans))


def mult():
    data.set("Matrix Multiplication")

    arr, arr1 = get_data(1)
    if arr is None or arr1 is None:
        return

    # Array multiplication
    ans = arr.dot(arr1)

    text.delete(1.0, END)
    text.insert(END, "Entered Matrix 1:\n" + str(arr)+"\n" + "Entered Matrix 2:" + "\n" + str(arr1))
    text.insert(END, "\n\nAnswer:\n"+str(ans))


def div():
    data.set("Matrix Division")

    arr, arr1 = get_data(1)
    if arr is None or arr1 is None:
        return

    # Array division
    ans = arr / arr1

    text.delete(1.0, END)
    text.insert(END, "Entered Matrix 1:\n" + str(arr) + "\n" + "Entered Matrix 2:" + "\n" + str(arr1))
    text.insert(END, "\n\nAnswer:\n"+str(ans))


def tran():
    data.set("Matrix Transpose")

    arr, arr1 = get_data(0)
    if arr is None or arr1 is None:
        return

    # Array transpose
    ans = np.transpose(arr)

    text.delete(1.0, END)
    text.insert(END, "Entered Matrix 1:\n" + str(arr))
    text.insert(END, "\n\nAnswer:\n" + str(ans))


def det():
    data.set("Matrix Determinant")

    arr, arr1 = get_data(0)
    if arr is None or arr1 is None:
        return

    # Array determinant
    ans = round(np.linalg.det(arr))

    text.delete(1.0, END)
    text.insert(END, "Entered Matrix 1:\n" + str(arr))
    text.insert(END, "\n\nAnswer:\n" + str(ans))


def inv():
    data.set("Matrix Inverse")

    arr, arr1 = get_data(0)
    if arr is None or arr1 is None:
        return

    # Array inverse
    ans = np.linalg.inv(arr)

    text.delete(1.0, END)
    text.insert(END, "Entered Matrix 1:\n" + str(arr))
    text.insert(END, "\n\nAnswer:\n" + str(ans))


def data_window(title, num):
    global mat1_data, mat2_data

    # Data box

    win = Toplevel()
    win.title(title)
    win.geometry("500x500")

    def ok():
        global mat1_data, mat2_data
        # Assigns the entered values to the variables
        if num == 1:
            mat1_data = str(space.get(1.0, END)).strip()
        elif num == 2:
            mat2_data = str(space.get(1.0, END)).strip()

        win.destroy()

    space = Text(win, font="Verdana 12", wrap="word", width=1, undo=TRUE)
    space.pack(expand=TRUE, fill=BOTH)
    space.focus()

    ok_btn = ttk.Button(win, text="OK", command=ok)
    ok_btn.pack(side=BOTTOM)

    if num == 1:
        space.insert(1.0, mat1_data)
    elif num == 2:
        space.insert(1.0, mat2_data)


def get_mat1():
    global mat1_data

    data_window("Matrix 1 Data: ", 1)


def get_mat2():
    global mat2_data

    data_window("Matrix 2 Data: ", 2)


def about_us():
    tm.showinfo("About Us", "This Code Is Written By Nikhil")


def helps():
    # This will be executed when help is clicked which is in about

    text.delete(1.0, END)
    text.insert(END, "1.Enter The Matrix By Clicking On Matrix 1 & 2 Data Buttons And Click OK To Save The Values\n")
    text.insert(END, "2.Press Space Bar After Each Value And Press Enter Key After Each Row And Leave No Extra Spaces\n")
    text.insert(END, "3.You Can Enter More Number Of Values By Maximizing The Data Window\n")
    text.insert(END, "4.You Can Scroll The Answer Box By Using Scroll Wheel Or UP & DOWN Arrows\n")
    text.insert(END, "5.You Can Quickly Write Something In The Answer Box\n")
    text.insert(END, "6.You Can select text In Answer Box By Pressing CTRL+A(OR)Drag With Mouse(OR)Press SHIFT+ARROWS\n")
    text.insert(END, "7.You Can Copy The Values By Pressing CTRL+C Keys\n")

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

mat1 = ttk.Button(left, text="\t\t\tMatrix 1 Data\t\t\t\t", command=get_mat1)
mat1.pack(padx=6, pady=6)

right = Frame(middle)
right.pack(side=RIGHT)

l2 = ttk.Label(right, text="Enter Matrix 2 Values : ")
l2.pack(padx=3, pady=3)

mat1 = ttk.Button(right, text="\t\t\tMatrix 2 Data\t\t\t\t", command=get_mat2)
mat1.pack(padx=6, pady=6)

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
