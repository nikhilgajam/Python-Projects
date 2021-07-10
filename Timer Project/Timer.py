from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import playsound
import threading

root = Tk()
root.title("Timer")
root.resizable(0, 0)

# Variables
start_var = False
set_var = True
sound_var = False

hours = 0
minutes = 0
seconds = 0


# Commands
def update():
    global hours, minutes, seconds, start_var, sound_var

    if start_var and seconds >= 0:
        if seconds == 0 and minutes != 0:
            seconds = 60
            minutes -= 1
        if seconds == 0 and minutes == 0 and hours != 0:
            hours -= 1
            minutes = 59
            seconds = 60
        seconds -= 1
        display['text'] = "%02d:%02d:%02d" % (hours, minutes, seconds)

    if start_var and hours == minutes == seconds == 0:
        sound_var = True
        start_var = False
        threading.Thread(target=play_sound).start()

    root.after(1000, update)


def set_reset(e=""):
    global set_var, start_var, sound_var, hours, minutes, seconds
    if set_var:     # Set
        set_window()
    else:           # Reset
        set_var = True
        start_var = False
        sound_var = False
        set_btn['text'] = "Set"
        hours = minutes = seconds = 0
        display['text'] = "%02d:%02d:%02d" % (hours, minutes, seconds)
        start_btn['text'] = "Start"


def start(e=""):
    global start_var, sound_var, set_var

    if (hours == minutes == seconds == 0) and (not sound_var):
        messagebox.showwarning("Warning", "Set The Time By Clicking On Set Button To Start The Timer")
        return

    if not start_var and not sound_var:  # Start
        start_var = True
        start_btn['text'] = "Stop"
    else:                                # Stop
        if sound_var:
            set_btn['text'] = "Set"
            set_var = True
        start_var = False
        sound_var = False
        start_btn['text'] = "Start"


def set_window():
    top = Toplevel()
    top.attributes("-toolwindow", 1)
    top.focus()
    top.grab_set()  # To make root window un-clickable

    # To position the top window depending on root
    x_pos = root.winfo_x()
    y_pos = root.winfo_y()
    top.geometry("+%d+%d" % (x_pos + 100, y_pos + 25))

    # Method to set time
    def set_time(e=""):
        global hours, minutes, seconds, set_var
        try:
            hours = int(hour_ent.get())
            minutes = int(minute_ent.get())
            seconds = int(second_ent.get())
            set_btn['text'] = "Reset"
            set_var = False
        except ValueError:
            messagebox.showerror("Error", "Enter Only Numbers In Hours, Minutes And Seconds Boxes")
            return

        display['text'] = "%02d:%02d:%02d" % (hours, minutes, seconds)
        top.destroy()

    # Labels, input boxes
    frame = Frame(top)
    frame.pack()

    hour_lbl = Label(frame, text="Hours   :")
    hour_lbl.grid(row=0, column=0, padx=6)

    hour_ent = Entry(frame, width=6)
    hour_ent.grid(row=0, column=1, padx=6)
    hour_ent.insert(0, "00")

    minute_lbl = Label(frame, text="Minutes : ")
    minute_lbl.grid(row=1, column=0, padx=6)

    minute_ent = Entry(frame, width=6)
    minute_ent.grid(row=1, column=1, padx=6)
    minute_ent.insert(0, "05")

    second_lbl = Label(frame, text="Seconds : ")
    second_lbl.grid(row=3, column=0, padx=6)

    second_ent = Entry(frame, width=6)
    second_ent.grid(row=3, column=1, padx=6)
    second_ent.insert(0, "00")
    second_ent.bind("<Return>", set_time)

    # Button
    set_time_btn = ttk.Button(top, text="Set", command=set_time)
    set_time_btn.pack(padx=6, pady=10)
    set_time_btn.bind("<Return>", set_time)


def play_sound():
    while sound_var:
        playsound.playsound("sounds/Alarm.mp3")


def close():
    global sound_var
    sound_var = False
    root.destroy()


# Display
display = Label(root, text="%02d:%02d:%02d" % (hours, minutes, seconds), font=("Times New Roman", 60))
display.pack(padx=10)

# Buttons
buttons = Frame(root)
buttons.pack()

set_btn = ttk.Button(buttons, text="Set", command=set_reset)
set_btn.grid(row=0, column=0, padx=8, pady=10)
set_btn.bind("<Return>", set_reset)

start_btn = ttk.Button(buttons, text="Start", command=start)
start_btn.grid(row=0, column=1, padx=8, pady=10)
start_btn.bind("<Return>", start)

# This will call update and it will run until program ends
update()

root.eval('tk::PlaceWindow . center')  # To place the window in center of screen
root.protocol('WM_DELETE_WINDOW', close)  # When pressed close run close
root.mainloop()
