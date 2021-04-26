from tkinter import *
import time

root = Tk()
root.title("Time")


def update():
    time_str = time.strftime("%I:%M:%S %p")
    # To know about different directives
    time_label['text'] = time_str

    day_date_str = time.strftime("%A\n%B %d, %Y")
    day_date_label['text'] = day_date_str

    # After method is defined in root window and label classes and it takes time in milliseconds and function
    root.after(1000, update)


time_label = Label(root, font=('Bell MT', 60), fg='#dadce0', bg='#35363a')
time_label.pack(fill=BOTH, expand=TRUE)

day_date_label = Label(root, font=('Bell MT', 40))
day_date_label.pack(fill=BOTH, expand=TRUE)

update()

root.mainloop()


'''



# TIME WITH THREADING (SOMETIMES IT MAY CRASH WHEN YOU TRY TO CLOSE THE WINDOW)

from datetime import datetime
from tkinter import *
import threading
import time
import sys

root = Tk()
root.title("Time")

l0 = Label(root, text="", font="Verdana 16")
l0.pack()
l1 = Label(root, text="", font="Verdana 40")
l1.pack()

var = True


def time_thing():

    while var:
        c = time.ctime(time.time())
        d = datetime.strptime(c[11:16], "%H:%M")
        d = d.strftime("%I:%M %p")
        d = d[:-3] + c[16:19] + d[5:]

        l1['text'] = d
        l0['text'] = " Day : " + c[:4] + "\n" + "Date  : " + c[8:11] + "\t" + " Year : " + c[20:] + "\n" + "Month: " + c[4:8]

    root.destroy()


def ok():
    global var
    var = False
    sys.exit()


t1 = threading.Thread(target=time_thing, args=())
t1.start()

root.protocol("WM_DELETE_WINDOW", ok)
root.mainloop()



'''
