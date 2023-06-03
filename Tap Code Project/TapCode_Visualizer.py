import tkinter
from tkinter import messagebox

# Window
window = tkinter.Tk()
window.title("Tap Code Visualizer")

# Variables
row_selected = False
col_selected = False
row_no = 0
col_no = 0
taps_display_text = ""
letters_display_text = ""

# Tap code table
TAP_CODE = [['A', 'B', 'C', 'D', 'E'],
            ['F', 'G', 'H', 'I', 'J'],
            ['L', 'M', 'N', 'O', 'P'], 
            ['Q', 'R', 'S', 'T', 'U'],
            ['V', 'W', 'X', 'Y', 'Z']]   # Row first and column next and we need to replace K with C

# Methods

def clearSelColors():
    # Clearing the selected colors
    for i in range(1, 6):
        for j in range(1, 6):
            tap_grid_labels[i][j].config(bg="SystemButtonFace")  # Setting to default color

def tapButtonPressed():
    global row_selected, col_selected, row_no, col_no

    if row_selected != True and row_no >= 5:
        row_no = 0

    if col_selected != True and col_no >= 5:
        col_no = 0

    clearSelColors()

    if not row_selected:
        for i in range(1, 6):
            tap_grid_labels[row_no + 1][i].config(bg="green")
        row_no += 1

    if row_selected is True and col_selected is not True:
        tap_grid_labels[row_no][col_no + 1].config(bg="green")
        col_no += 1

    now_taps_display['text'] = ("."*row_no) + " " + ("."*col_no)


def lockButtonPressed():
    global row_selected, col_selected, row_no, col_no

    if row_no == 0:
        tapButtonPressed()
    
    if not row_selected:
        row_selected = True
    
    if row_selected:
        col_no = 0

    clearSelColors()
    
    tapButtonPressed()


def selectButtonPressed():
    global row_selected, col_selected, row_no, col_no, taps_display_text, letters_display_text

    if row_selected:
        taps_display_text += ("."*row_no) + " " + ("."*col_no) + "/"
        letters_display_text += TAP_CODE[row_no-1][col_no-1]
        taps_display['text'] = taps_display_text
        letters_display['text'] = letters_display_text
        row_no = 0
        col_no = 0
        row_selected = False
        col_selected = False
        tapButtonPressed()
    else:
        messagebox.showwarning("Warning", "Select a row by clicking on the Lock Row button and select " +
        "a column with Tap button then click Select Column button")


def spaceButtonPressed():
    global taps_display_text, letters_display_text

    if letters_display == "":
        return

    taps_display_text += "/"
    letters_display_text += " "

    taps_display['text'] = taps_display_text
    letters_display['text'] = letters_display_text

# Widgets

# Heading label
heading = tkinter.Label(window, text="Tap Code Visualizer", font=("Times New Roman", 28))
heading.pack(padx=10, pady=26)

# Tap code grid area
tap_grid_area = tkinter.Frame(window)
tap_grid_area.pack()

# Tap code labels
tap_grid_labels = [[tkinter.Label(tap_grid_area) for j in range(6)] for i in range(6)]
for i in range(6):
    for j in range(6):
        tap_grid_labels[i][j].config(font=("Times New Roman", 22))

        if i != 0 and j != 0:
            tap_grid_labels[i][j].config(text=TAP_CODE[i-1][j-1])
        
        if i == 0 and j != 0:
            tap_grid_labels[i][j].config(text=str(j), fg="grey")

        if i != 0 and j == 0:
            tap_grid_labels[i][j].config(text=str(i)+" ", fg="grey")
        
        tap_grid_labels[i][j].grid(row=i, column=j, padx=1)

# Buttons area
buttons_area = tkinter.Frame(window)
buttons_area.pack(pady=10)

# Tap button
tap_btn = tkinter.Button(buttons_area, text="Tap", 
command=tapButtonPressed)
tap_btn.grid(row=0, column=0, padx=4, pady=4)

# Lock row button
lock_btn = tkinter.Button(buttons_area, text="Lock Row",
command=lockButtonPressed)
lock_btn.grid(row=0, column=1, padx=4, pady=4)

# Select column button
select_btn = tkinter.Button(buttons_area, text="Select Column",
command=selectButtonPressed)
select_btn.grid(row=0, column=2, padx=4, pady=4)

# Space button
space_btn = tkinter.Button(buttons_area, text="Space",
command=spaceButtonPressed)
space_btn.grid(row=0, column=3, padx=4, pady=4)

# Now taps display
now_taps_display = tkinter.Label(window, font=("Times New Roman", 28), text="")
now_taps_display.pack()

# Letters display
letters_display = tkinter.Label(window, font=("Times New Roman", 22), text="")
letters_display.pack(padx=4)

taps_display = tkinter.Label(window, font=("Times New Roman", 22), text="")
taps_display.pack()

window.mainloop()
