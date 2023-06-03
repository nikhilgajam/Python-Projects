from tkinter import messagebox
import tkinter
import random
import webbrowser
import HashingSaving

# Variables
INITIAL_SYMBOLS = ['☀', '☎', '☕']  # We can use symbols like this ['🦄', '🍇', '🍔'] also
INITIAL_SYMBOL_CLICKED = ''
INITIAL_SYMBOL_1_ELEMENTS = [['▟', '▞', '▝'], ['▜', '▛', '▚'], ['▙', '▉', '▅']]
INITIAL_SYMBOL_2_ELEMENTS = [['ᙗ', 'ᘚ', 'ᗍ'], ['ᕒ', 'ᑬ', 'ლ'], ['፴', '፳', 'ቖ']]
INITIAL_SYMBOL_3_ELEMENTS = [['╦', '╠', '╬'], ['╭', '╮', '╳'], ['╏', '╯', '╰']]
INITIAL_SYMBOL_SELECTED = False
SYMBOL_SELECTED_SEQUENCE = []
SELECTED_SYMBOL = ""
USER_NAME = ""
PASSWORD = ""

# Window settings
window = tkinter.Tk()
window.geometry("800x500")


# Methods


def clear_screen(win):    # Removes all the widgets on the window
    _list = win.winfo_children()

    for item in _list :
        if item.winfo_children() :
            _list.extend(item.winfo_children())

    for widget in _list:
        widget.pack_forget()


def mainPage():
    # Window Title And Headings
    window.title("Graphical Password Authentication")

    heading = tkinter.Label(window, text="Graphical Password Authentication", font=("Times New Roman", 30))
    heading.pack(pady=10)

    # Buttons
    sign_in_btn = tkinter.Button(window, text="Sign In", font=("Times New Roman", 25), command=signInPage)
    sign_in_btn.pack(pady=20)

    sign_up_btn = tkinter.Button(window, text="Sign Up", font=("Times New Roman", 25), command=signUpPage)
    sign_up_btn.pack(pady=20)

    # Instruction label
    instruction_lbl = tkinter.Label(window, text="Welcome...\nPress Sign In If You Have An Account Otherwise Press Sign Up", font=("Times New Roman", 20))
    instruction_lbl.pack(pady=10)

    # Setting the values to default
    setDefaultVariables()


def buttonClicked(btn, btn1, btn2, next_btn, symbol, username, password):
    global INITIAL_SYMBOL_SELECTED, INITIAL_SYMBOL_CLICKED, SELECTED_SYMBOL, USER_NAME, PASSWORD

    if username.get() == "":
        messagebox.showwarning("Warning", "Please Type Username")
        return
    if password.get() == "":
        messagebox.showwarning("Warning", "Please Type Password")
        return
    
    USER_NAME = username.get()
    PASSWORD = password.get()

    INITIAL_SYMBOL_SELECTED = True
    INITIAL_SYMBOL_CLICKED = btn['text']
    next_btn.config(state=tkinter.NORMAL)
    btn.config(bg='green')
    btn1.config(bg='SystemButtonFace')
    btn2.config(bg='SystemButtonFace')
    SELECTED_SYMBOL = symbol


def setDefaultVariables():
    # Setting the values to default
    global USER_NAME, PASSWORD, INITIAL_SYMBOL_SELECTED, SELECTED_SYMBOL, INITIAL_SYMBOL_CLICKED

    SYMBOL_SELECTED_SEQUENCE.clear()
    USER_NAME = ""
    PASSWORD = ""
    SELECTED_SYMBOL = ""
    INITIAL_SYMBOL_SELECTED = False
    INITIAL_SYMBOL_CLICKED = ''


def backButtonClicked(name):
    clear_screen(window)  # Removes all the widgets on the window

    setDefaultVariables()

    # Redirecting to the before pages
    if name == "Sign Up" or name == "Sign In":
        mainPage()
    if name == "Grid Sign Up":
        signUpPage()
    if name == "Grid Sign In":
        signInPage()


def signUpPage():
    global INITIAL_SYMBOL_SELECTED

    clear_screen(window)  # Removes all the widgets on the window

    # Window title and headings
    window.title("Sign Up Page")

    heading = tkinter.Label(window, text="Graphical Password Authentication\nSign Up", font=("Times New Roman", 30))
    heading.pack(pady=10)

    # Back button
    back_btn = tkinter.Button(window, text="Back", command=lambda: backButtonClicked("Sign Up"))
    back_btn.pack(anchor=tkinter.NW)

    # User name and password area
    box_area = tkinter.Frame(window)
    box_area.pack()

    username_lbl = tkinter.Label(box_area, text="Username: ")
    username_lbl.grid(row=0, column=0)

    username_box = tkinter.Entry(box_area)
    username_box.grid(row=0, column=1)

    password_lbl = tkinter.Label(box_area, text="Password: ")
    password_lbl.grid(row=1, column=0)

    password_box = tkinter.Entry(box_area, show='*')
    password_box.grid(row=1, column=1)

    random.shuffle(INITIAL_SYMBOLS)  # Shuffling the symbols

    # Symbol area
    symbol_area = tkinter.Frame(window)
    symbol_area.pack(pady=10)

    symbol_1_btn = tkinter.Button(symbol_area, text=INITIAL_SYMBOLS[0], font=("Times New Roman", 40))
    symbol_1_btn.grid(row=0, column=0, padx=6)

    symbol_2_btn = tkinter.Button(symbol_area, text=INITIAL_SYMBOLS[1], font=("Times New Roman", 40))
    symbol_2_btn.grid(row=0, column=1, padx=6)

    symbol_3_btn = tkinter.Button(symbol_area, text=INITIAL_SYMBOLS[2], font=("Times New Roman", 40))
    symbol_3_btn.grid(row=0, column=2, padx=6)

    # Next button
    next_btn = tkinter.Button(window, text="Next", state=tkinter.DISABLED, command=lambda: gridPage('Register'))
    next_btn.pack(pady=10)

    # Symbol command configuration
    symbol_1_btn.config(command=lambda: buttonClicked(symbol_1_btn, symbol_2_btn, symbol_3_btn, next_btn, INITIAL_SYMBOLS[0], username_box, password_box))
    symbol_2_btn.config(command=lambda: buttonClicked(symbol_2_btn, symbol_1_btn, symbol_3_btn, next_btn, INITIAL_SYMBOLS[1], username_box, password_box))
    symbol_3_btn.config(command=lambda: buttonClicked(symbol_3_btn, symbol_1_btn, symbol_2_btn, next_btn, INITIAL_SYMBOLS[2], username_box, password_box))


def signInPage():
    global INITIAL_SYMBOL_SELECTED

    clear_screen(window)  # Removes all the widgets on the window

    # Window title and headings
    window.title("Sign In Page")

    heading = tkinter.Label(window, text="Graphical Password Authentication\nSign In", font=("Times New Roman", 30))
    heading.pack(pady=10)

    # Back button
    back_btn = tkinter.Button(window, text="Back", command=lambda: backButtonClicked("Sign In"))
    back_btn.pack(anchor=tkinter.NW)

    # User name and password area
    box_area = tkinter.Frame(window)
    box_area.pack()

    username_lbl = tkinter.Label(box_area, text="Username: ")
    username_lbl.grid(row=0, column=0)

    username_box = tkinter.Entry(box_area)
    username_box.grid(row=0, column=1)

    password_lbl = tkinter.Label(box_area, text="Password: ")
    password_lbl.grid(row=1, column=0)

    password_box = tkinter.Entry(box_area, show='*')
    password_box.grid(row=1, column=1)

    random.shuffle(INITIAL_SYMBOLS)  # Shuffling the symbols

    # Symbol area
    symbol_area = tkinter.Frame(window)
    symbol_area.pack(pady=10)

    symbol_1_btn = tkinter.Button(symbol_area, text=INITIAL_SYMBOLS[0], font=("Times New Roman", 40))
    symbol_1_btn.grid(row=0, column=0, padx=6)

    symbol_2_btn = tkinter.Button(symbol_area, text=INITIAL_SYMBOLS[1], font=("Times New Roman", 40))
    symbol_2_btn.grid(row=0, column=1, padx=6)

    symbol_3_btn = tkinter.Button(symbol_area, text=INITIAL_SYMBOLS[2], font=("Times New Roman", 40))
    symbol_3_btn.grid(row=0, column=2, padx=6)

    # Next button
    next_btn = tkinter.Button(window, text="Next", state=tkinter.DISABLED, command=nextSignIn)
    next_btn.pack(pady=10)

    # Symbol command configuration
    symbol_1_btn.config(command=lambda: buttonClicked(symbol_1_btn, symbol_2_btn, symbol_3_btn, next_btn, INITIAL_SYMBOLS[0], username_box, password_box))
    symbol_2_btn.config(command=lambda: buttonClicked(symbol_2_btn, symbol_1_btn, symbol_3_btn, next_btn, INITIAL_SYMBOLS[1], username_box, password_box))
    symbol_3_btn.config(command=lambda: buttonClicked(symbol_3_btn, symbol_1_btn, symbol_2_btn, next_btn, INITIAL_SYMBOLS[2], username_box, password_box))


def gridButtonsClicked(btn, next_btn):
    if btn['bg'] == 'SystemButtonFace':
        btn['bg'] = 'green'
        SYMBOL_SELECTED_SEQUENCE.append(btn['text'])
    else:
        btn['bg'] = 'SystemButtonFace'
        SYMBOL_SELECTED_SEQUENCE.remove(btn['text'])
    
    gridCalculate(next_btn)


def gridCalculate(next_btn):
    global SYMBOL_SELECTED_SEQUENCE

    if len(SYMBOL_SELECTED_SEQUENCE) >= 3:
        next_btn['state'] = tkinter.NORMAL
    else:
        next_btn['state'] = tkinter.DISABLED


def nextSignIn():
    read_data = end_read()  # Reading the data
    hs = HashingSaving.HashSave()  # Hashing the password to check with the stored password
    hashed = hs.hash(PASSWORD)

    if len(read_data) == 0:
        messagebox.showwarning("Warning", "Type Correct Username And Password")
        setDefaultVariables()
        return

    if USER_NAME == read_data[0][0] and hashed == read_data[0][1] and SELECTED_SYMBOL == read_data[0][2]:
        gridPage('Sign In')
    else:
        messagebox.showwarning("Warning", "Type Correct Username And Password")
        setDefaultVariables()


def endSignIn():
        read_data = end_read()
        if read_data[0][3] == "".join(SYMBOL_SELECTED_SEQUENCE):
            yn = messagebox.askyesno("Successfully Signed In", "Your Credentials Are Validated Successfully.\nDo you want to open the website")
            if yn:
                webbrowser.open("google.com")
                clear_screen(window)
                mainPage()
        else:
            messagebox.showwarning("Warning", "Select the correct sequence")

def endRegister():
    end_save()
    messagebox.showinfo("Thank you for registering!!!", "Registration Is Complete, Please Sign In")
    SYMBOL_SELECTED_SEQUENCE.clear()
    # Clearing the screen and loading the main page
    clear_screen(window)
    mainPage()


def end_save():
    # Saves the whole data into database and also hashes the password
    hs = HashingSaving.HashSave()
    hashed = hs.hash(PASSWORD)  # Hashing the password
    hs.save_in_db(USER_NAME, hashed, INITIAL_SYMBOL_CLICKED, "".join(SYMBOL_SELECTED_SEQUENCE))

def end_read():
    # Returns the saved data when USER_NAME is given
    hs = HashingSaving.HashSave()
    return hs.read_db(USER_NAME)

def gridPage(btn_name):
    # Creates the grid page which will be presented after sign up or sign in
    clear_screen(window)  # Removes all the widgets on the window

    heading = tkinter.Label(window, text="Graphical Password Authentication", font=("Times New Roman", 30))
    heading.pack(pady=10)

    # Back button
    back_btn = tkinter.Button(window, text="Back")
    back_btn.pack(anchor=tkinter.NW)

    # Instruction label
    lbl = tkinter.Label(window, text="Select Minimum 3 Boxes Of Your Choice")
    lbl.pack()

    # Grid area
    grid_area = tkinter.Frame(window)
    grid_area.pack()

    INITIAL_SYMBOL_K_ELEMENTS = None  # Selected symbol shuffled list pointer variable

    if SELECTED_SYMBOL == '☀':
        random.shuffle(INITIAL_SYMBOL_1_ELEMENTS)  # Shuffling the symbols
        INITIAL_SYMBOL_K_ELEMENTS = INITIAL_SYMBOL_1_ELEMENTS
    if SELECTED_SYMBOL == '☎':
        random.shuffle(INITIAL_SYMBOL_2_ELEMENTS)  # Shuffling the symbols
        INITIAL_SYMBOL_K_ELEMENTS = INITIAL_SYMBOL_2_ELEMENTS
    if SELECTED_SYMBOL == '☕':
        random.shuffle(INITIAL_SYMBOL_3_ELEMENTS)  # Shuffling the symbols
        INITIAL_SYMBOL_K_ELEMENTS = INITIAL_SYMBOL_3_ELEMENTS

    btn1 = tkinter.Button(grid_area, text=INITIAL_SYMBOL_K_ELEMENTS[0][0], font=("Times New Roman", 40))
    btn1.grid(row=0, column=0)
    btn2 = tkinter.Button(grid_area, text=INITIAL_SYMBOL_K_ELEMENTS[0][1], font=("Times New Roman", 40))
    btn2.grid(row=0, column=1)
    btn3 = tkinter.Button(grid_area, text=INITIAL_SYMBOL_K_ELEMENTS[0][2], font=("Times New Roman", 40))
    btn3.grid(row=0, column=2)
    btn4 = tkinter.Button(grid_area, text=INITIAL_SYMBOL_K_ELEMENTS[1][0], font=("Times New Roman", 40))
    btn4.grid(row=1, column=0)
    btn5 = tkinter.Button(grid_area, text=INITIAL_SYMBOL_K_ELEMENTS[1][1], font=("Times New Roman", 40))
    btn5.grid(row=1, column=1)
    btn6 = tkinter.Button(grid_area, text=INITIAL_SYMBOL_K_ELEMENTS[1][2], font=("Times New Roman", 40))
    btn6.grid(row=1, column=2)
    btn7 = tkinter.Button(grid_area, text=INITIAL_SYMBOL_K_ELEMENTS[2][0], font=("Times New Roman", 40))
    btn7.grid(row=2, column=0)
    btn8 = tkinter.Button(grid_area, text=INITIAL_SYMBOL_K_ELEMENTS[2][1], font=("Times New Roman", 40))
    btn8.grid(row=2, column=1)
    btn9 = tkinter.Button(grid_area, text=INITIAL_SYMBOL_K_ELEMENTS[2][2], font=("Times New Roman", 40))
    btn9.grid(row=2, column=2)

    # Next Button
    next_btn = tkinter.Button(window, text=btn_name, state=tkinter.DISABLED)
    next_btn.pack()

    # Grid button command configuration
    btn1.config(command=lambda: gridButtonsClicked(btn1, next_btn))
    btn2.config(command=lambda: gridButtonsClicked(btn2, next_btn))
    btn3.config(command=lambda: gridButtonsClicked(btn3, next_btn))
    btn4.config(command=lambda: gridButtonsClicked(btn4, next_btn))
    btn5.config(command=lambda: gridButtonsClicked(btn5, next_btn))
    btn6.config(command=lambda: gridButtonsClicked(btn6, next_btn))
    btn7.config(command=lambda: gridButtonsClicked(btn7, next_btn))
    btn8.config(command=lambda: gridButtonsClicked(btn8, next_btn))
    btn9.config(command=lambda: gridButtonsClicked(btn9, next_btn))

    # Assigns next button to the commands particular to the invoked button or method
    if btn_name == "Register":
        next_btn.config(command=endRegister)
        back_btn.config(command=lambda: backButtonClicked("Grid Sign Up"))
    else:
        next_btn.config(command=endSignIn)
        back_btn.config(command=lambda: backButtonClicked("Grid Sign In"))


# Loading the main page
mainPage()

# Mainloop statement
window.mainloop()
