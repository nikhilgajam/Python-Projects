from tkinter import *


# Main window
window = Tk()
window.config(bg="#333333")
window.title("StopWatch")

# Variables
started = False
lap_count = 0

hours = 0
minutes = 0
seconds = 0
millis = 0


# Commands

def update():
    global hours, minutes, seconds, millis

    if started:
        millis += 1
        if millis == 1000:
            seconds += 1
            millis = 0
        elif seconds == 60:
            minutes += 1
            seconds = 0
        elif minutes == 60:
            hours += 1
            minutes = 0
        time_display['text'] = "%02d:%02d:%02d.%03d" % (hours, minutes, seconds, millis)

    window.after(1, update)


def start():
    global started
    if not started:
        started = True
        start_btn['text'] = "Stop"
    else:
        started = False
        start_btn['text'] = "Start"


def reset():
    global hours, minutes, seconds, millis, started
    started = False
    start_btn['text'] = "Start"
    hours = minutes = seconds = millis = 0
    time_display['text'] = "00:00:00.000"


def lap():
    global lap_count
    lap_count += 1
    lap_display['state'] = NORMAL
    lap_display.insert(END, "%d.  %02d:%02d:%02d.%03d\n" % (lap_count, hours, minutes, seconds, millis))
    lap_display['state'] = DISABLED
    lap_display.yview(END)  # Auto Scroll


# Time display label
time_display = Label(window, text="00:00:00.000", font=("Times New Roman", 50), fg="#e6e8eb", bg="#333333")
time_display.pack()

# Buttons
buttons = Frame(window, bg="#333333")
buttons.pack()

start_btn = Button(buttons, text="Start", font=("Harlow Solid Italic", 15), command=start, fg="#e6e8eb",
                   bg="#333333", activebackground="gray")
start_btn.grid(row=0, column=1, padx=10, pady=6)

reset_btn = Button(buttons, text="Reset", font=("Harlow Solid Italic", 15), command=reset, fg="#e6e8eb",
                   bg="#333333", activebackground="gray")
reset_btn.grid(row=0, column=2, padx=10, pady=6)

lap_btn = Button(buttons, text="Lap", font=("Harlow Solid Italic", 15), command=lap, fg="#e6e8eb",
                 bg="#333333", activebackground="gray")
lap_btn.grid(row=0, column=3, padx=10, pady=6)


# Lap display label
lap_display = Text(window, fg="#e6e8eb", bg="#333333", insertbackground="#333333", state=DISABLED,
                   font=("Times New Roman", ), height=8, width=50)
lap_display.pack(fill=BOTH, expand=TRUE)

update()

window.eval('tk::PlaceWindow . center')  # To place the window in center of screen
window.mainloop()
