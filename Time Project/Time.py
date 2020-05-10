from datetime import datetime
from tkinter import *
import threading
import time

root = Tk()
root.title("Time")

l0 = Label(root, text="", font="Verdana 16")
l0.pack()
l1 = Label(root, text="", font="Verdana 40")
l1.pack()


def time_thing(i=0):

    while TRUE:
        c = time.ctime(time.time())
        d = datetime.strptime(c[11:16], "%H:%M")
        d = d.strftime("%I:%M %p")
        d = d[:-3] + c[16:19] + d[5:]

        if i > 0:
            time.sleep(1)

        l1['text'] = d
        l0['text'] = " Day : " + c[:4] + "\n" + "Date  : " + c[8:11] + "\t" + " Year : " + c[20:] + "\n" + "Month: " + c[4:8]

        i += 1


def ok():
    root.destroy()


t1 = threading.Thread(target=time_thing)
t1.start()

root.protocol("WM_DELETE_WINDOW", ok)
root.mainloop()
