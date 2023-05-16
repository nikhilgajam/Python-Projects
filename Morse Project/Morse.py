import tkinter
from tkinter import messagebox
import wave
import threading
import subprocess
import time

# Window
window = tkinter.Tk()
window.title("Morse Code")
window.geometry("660x440")

# Morse Code
eng_to_morse = {'A':'.-', 'B':'-...', 'C':'-.-.', 'D':'-..', 'E':'.', 'F':'..-.', 'G':'--.', 'H':'....', 'I':'..', 
'J':'.---', 'K':'-.-', 'L':'.-..', 'M':'--', 'N':'-.', 'O':'---', 'P':'.--.', 'Q':'--.-', 'R':'.-.', 'S':'...', 
'T':'-', 'U':'..-', 'V':'...-', 'W':'.--', 'X':'-..-', 'Y':'-.--', 'Z':'--..', '1':'.----', '2':'..---', 
'3':'...--', '4':'....-', '5':'.....', '6':'-....', '7':'--...', '8':'---..', '9':'----.', '0':'-----', ',':'--..--', 
'.':'.-.-.-', '?':'..--..', ':':'---...', ';':'_._._.', '\'':'.----.', '"':'.-..-.', '(':'-.--.', ')':'-.--.-', 
'+':'.-.-.', '-':'-....-', '=':'-...-', '_':'..--.-', '@':'.--.-.', '!':'-.-.--', '&':'.-...', '/':'-..-.', ' ':' '}
morse_to_eng = dict([(v, k) for k, v in eng_to_morse.items()])  # Changing the values to keys and keys to values in dictionary

# Variables
morse_code_sound_path = ""
eng_to_morse_path = ""
morse_to_eng_path = ""

# Methods


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


def morseToSound(data : str):
    # Binding dots, dashes and spaces into file names to merge
    l = []

    for i in data:
        if i == '.':
            l.append("dot")
        elif i == '-':
            l.append("dash")
        elif i == ' ':
            l.append("space")

    waveMerger(l, morse_code_sound_path)

    run(morse_code_sound_path)


def engToMorse():
    # Converts english letters to morse code
    global morse_code_sound_path, eng_to_morse_path

    inp = input.get("1.0", tkinter.END).upper()

    if inp == "":
        tkinter.messagebox.showwarning("Warning", "Try to enter some text in the box.")
        return

    data = ""

    for i in inp:
        x = eng_to_morse.get(i)
        if x != None:
            data += x + ' '

    temp_time = time.ctime().replace(" ", "_").replace(":", "_")

    eng_to_morse_path = "English_To_Morse_" + temp_time + ".txt"
    morse_code_sound_path = "Morse_Code_" + temp_time + ".wav"

    writeOperation(eng_to_morse_path, data)
    morseToSound(data[:-1])

    run(eng_to_morse_path)

    input.focus()


def morseToEng():
    # Converts morse code to english letters
    global morse_to_eng_path

    inp = input.get("1.0", tkinter.END)

    if inp == "":
        tkinter.messagebox.showwarning("Warning", "Try to enter some text in the box.")
        return

    inp = inp.replace('\n', '').replace('\t', '')
    inp = inp.split(" ")
    data = ""

    for i in inp:
        if i != "":
            x = morse_to_eng.get(i)
            if x != None:
                data += x

    temp_time = time.ctime().replace(" ", "_").replace(":", "_")

    morse_to_eng_path = "Morse_To_English_" + temp_time + ".txt"
    writeOperation(morse_to_eng_path, data)

    run(morse_to_eng_path)

    input.focus()


# Heading label
heading = tkinter.Label(window, text="Morse Code", font=("Times New Roman", 28))
heading.pack(fill=tkinter.BOTH, expand=tkinter.TRUE)

# Input box
input = tkinter.Text(window, font=("Times New Roman", 20), height=8)
input.focus()
input.pack(fill=tkinter.BOTH, expand=tkinter.TRUE)

# Buttons area
buttons_area = tkinter.Frame(window)
buttons_area.pack(expand=tkinter.TRUE)

# English to morse button
eng_to_morse_btn = tkinter.Button(buttons_area, text="English To Morse", 
command=lambda: threading.Thread(target=engToMorse).start())
eng_to_morse_btn.grid(row=0, column=0, padx=4, pady=4)

# Morse to english
morse_to_eng_btn = tkinter.Button(buttons_area, text="Morse To English", 
command=lambda: threading.Thread(target=morseToEng).start())
morse_to_eng_btn.grid(row=0, column=1, padx=4, pady=4)

window.mainloop()
