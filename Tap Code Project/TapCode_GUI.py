import tkinter
from tkinter import messagebox
import wave
import threading
import subprocess
import time
import TapCodeAPI

# Window
window = tkinter.Tk()
window.title("Tap Code")
window.geometry("660x440")

# Variables
tap_code_sound_path = ""
eng_to_tap_path = ""
tap_to_eng_path = ""
tap_obj = TapCodeAPI.TapCode()

TAP_CODE = TapCodeAPI.TAP_CODE_TABLE

# Methods

def waveMerger(infiles : list, outfile : str):
    # This method merges the wave files
    try:
        data = []
        for infile in infiles:
            w = wave.open("sounds/" + infile + ".wav", 'rb')
            data.append([w.getparams(), w.readframes(w.getnframes())])
            w.close()
            
        output = wave.open(outfile, 'wb')
        output.setparams(data[0][0])
        for i in range(len(data)):
            output.writeframes(data[i][1])
        output.close()
    except Exception as e:
        print(e)
        messagebox.showerror("Error (Wave Merger)", e)


def writeOperation(path : str, data : str):
    # Writes data to the disk
    try:
        p = open(path, "w")
        p.write(data)
        p.close()
    except Exception as e:
        messagebox.showerror("Error (Write Operation)", e)


def run(path : str):
    # Runs the given document or file using cmd
    cmd = subprocess.Popen(path, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    output = str(cmd.stderr.read(), "utf-8")

    if output != "":
        messagebox.showerror("Error (Run)", output)


def tapToSound(data : str):
    # Binding taps and spaces into file names to merge
    l = []

    for i in data:
        if i == '.':
            l.append("tap")
        elif i == ' ':
            l.append("space")
        elif i == '/':
            l.append('space')

    waveMerger(l, tap_code_sound_path)

    run(tap_code_sound_path)


def engToTap():
    # Converts english letters to tap code
    global tap_code_sound_path, eng_to_tap_path

    inp = input.get("1.0", tkinter.END).upper()

    if inp == "":
        tkinter.messagebox.showwarning("Warning", "Try to enter some text in the box.")
        return

    inp = inp.replace("K", "C")  # Replacing all K letters with C because K is not used in tap code
    inp = inp.replace('\n', '').replace('\t', '')
    input.delete("1.0", tkinter.END)
    input.insert("1.0", inp)  # Displayed the replaced input on the screen

    data = tap_obj.englishToTapCode(input.get("1.0", tkinter.END))

    temp_time = time.ctime().replace(" ", "_").replace(":", "_")

    eng_to_morse_path = "English_To_Tap_Code_" + temp_time + ".txt"
    tap_code_sound_path = "Tap_Code_" + temp_time + ".wav"

    writeOperation(eng_to_morse_path, data)
    tapToSound(data)

    run(eng_to_morse_path)

    input.focus()


def tapToEng():
    # Converts tap code to english letters
    global tap_to_eng_path

    inp = input.get("1.0", tkinter.END)

    if inp == "":
        tkinter.messagebox.showwarning("Warning", "Try to enter some text in the box.")
        return

    data = tap_obj.tapCodeToEnglish(inp)

    temp_time = time.ctime().replace(" ", "_").replace(":", "_")

    morse_to_eng_path = "Tap_Code_To_English_" + temp_time + ".txt"
    writeOperation(morse_to_eng_path, data)

    run(morse_to_eng_path)

    input.focus()


# Heading label
heading = tkinter.Label(window, text="Tap Code", font=("Times New Roman", 28))
heading.pack(fill=tkinter.BOTH, expand=tkinter.TRUE)

# Input box
input = tkinter.Text(window, font=("Times New Roman", 20), height=8)
input.focus()
input.pack(fill=tkinter.BOTH, expand=tkinter.TRUE)

# Buttons area
buttons_area = tkinter.Frame(window)
buttons_area.pack(expand=tkinter.TRUE)

# English to tap code button
eng_to_tap_btn = tkinter.Button(buttons_area, text="English To Tap Code", 
command=lambda: threading.Thread(target=engToTap).start())
eng_to_tap_btn.grid(row=0, column=0, padx=4, pady=4)

# Tap code to english button
tap_to_eng_btn = tkinter.Button(buttons_area, text="Tap Code To English", 
command=lambda: threading.Thread(target=tapToEng).start())
tap_to_eng_btn.grid(row=0, column=1, padx=4, pady=4)

window.mainloop()
