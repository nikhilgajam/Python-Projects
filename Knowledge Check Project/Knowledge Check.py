from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
import urllib.request as req
import playsound
import threading
import html
import random

# Window
root = Tk()
root.config(bg="#333333")
root.title("Knowledge Check")
root.geometry("600x440")
root.iconbitmap(True, "images/icon.ico")

# Variables
data = ""
question = ""
correct_option = ""
ques_category = 9
ques_difficulty = ""  # easy or medium or hard
question_type = "multiple"  # or boolean
correct_option_index = -1
options = []
correct_score = wrong_score = 0
answer_check = ""
sound_var = BooleanVar(value=True)
ques_category_selected = "Categories"
ques_difficulty_selected = "Difficulty"
ques_type_selected = "Type"


# Commands

def load_question(var):
    global data, correct_option_index

    try:
        # Runs if and else according to the ques_difficulty which is matched
        if ques_difficulty == "":
            if ques_category_selected == "Categories":
                url = req.urlopen("https://opentdb.com/api.php?amount=1&type=" +
                                  question_type)  # Getting the data from Open Trivia Database
            else:
                url = req.urlopen("https://opentdb.com/api.php?amount=1&category=" + str(ques_category) + "&type=" +
                                  question_type)  # Getting the data from Open Trivia Database
        else:
            url = req.urlopen("https://opentdb.com/api.php?amount=1&category=" + str(ques_category) + "&difficulty=" +
                              ques_difficulty + "&type=" + question_type)  # Getting the data from Open Trivia Database
        data = data.replace("\\/", "/")  # Replaces \/ with /
        data = url.read().decode('unicode-escape')  # decode() can also be used
        data = html.unescape(data)   # Converting html text to plain text

        if var == 1:
            # Displays present question and loads next question
            display_and_load_next_question()

    except Exception:
        # Correct option index is going to be -1 when the question is not loaded completely
        correct_option_index = -1

        question_display['state'] = NORMAL
        question_display.delete(1.0, END)
        question_display.insert(END, "Check Your Internet Connection And Restart The Program")
        question_display['state'] = DISABLED


def display_and_load_next_question():
    global data, question, correct_option, correct_option_index, answer_check

    try:
        # Correct option index is going to be -1 when the question is not loaded completely
        correct_option_index = -1

        # Previous answer display
        if question != "":
            answer_check = question + "  (Ans: " + correct_option + ")"
            prev_ans_display['state'] = NORMAL
            prev_ans_display.delete(1.0, END)
            prev_ans_display.insert(END, answer_check)
            prev_ans_display['state'] = DISABLED

        # Question substring
        start = data.find('question":') + 11
        end = data.find('","correct_answer', start)
        question = data[start:end]
        question_display['state'] = NORMAL
        question_display.delete(1.0, END)  # Clears the question_display
        question_display.insert(END, question + "\n\n")

        # Correct option
        start = data.find('"correct_answer":') + 18
        end = data.find('",', start)
        correct_option = data[start:end]

        # Other options
        start = data.find('"incorrect_answers":["') + 22
        end = data.find('"]', start)
        other_options = data[start:end]

        options.clear()
        options.append(correct_option)
        for i in other_options.split('","'):
            options.append(i)

        random.shuffle(options)
        c = 65
        for i in range(len(options)):
            if options[i] == correct_option:
                correct_option_index = i
            question_display.insert(END, chr(c) + ".) " + options[i] + "\n")
            c += 1

        question_display['state'] = DISABLED

        # Loads the next question and 0 means don't display loaded question on the question_display
        threading.Thread(target=load_question, args=(0, )).start()

    except Exception as e:
        messagebox.showerror("Error", e)


def validate(num):
    global correct_score, wrong_score

    if correct_option_index != -1:
        if num == correct_option_index:
            correct_score += 1
            if sound_var.get():
                threading.Thread(target=play_audio, args=(True, )).start()
        else:
            wrong_score += 1
            if sound_var.get():
                threading.Thread(target=play_audio, args=(False, )).start()

        score_lbl['text'] = "Correct: " + str(correct_score) + " \t\t   Wrong: " + str(wrong_score)
        display_and_load_next_question()

    else:
        messagebox.showwarning("Warning", "Question is not yet loaded, wait till it loads")


def play_audio(var):
    # Plays sounds depending upon n value
    if var:
        playsound.playsound("sounds/correct.wav")
    else:
        playsound.playsound("sounds/wrong.wav")


def btn1_command(event=""):
    validate(0)


def btn2_command(event=""):
    validate(1)


def btn3_command(event=""):
    # When boolean type is used this button is disabled
    if question_type != "boolean":
        validate(2)
    else:
        messagebox.showwarning("Warning", "You Need To Use 1, 2 (OR) A, B Buttons When True/False Type Is "
                                          "Selected")


def btn4_command(event=""):
    # When boolean type is used this button is disabled
    if question_type != "boolean":
        validate(3)
    else:
        messagebox.showwarning("Warning", "You Need To Use 1, 2 (OR) A, B Buttons When True/False Type Is "
                                          "Selected")


def settings():
    global ques_category_selected, ques_difficulty_selected, ques_type_selected
    # This is used to open the settings window
    top = Toplevel(root, bg="#333333")
    top.title("Knowledge Check Settings")
    top.resizable(0, 0)
    top.focus()
    top_title = Label(top, text="Knowledge Check Settings", font=("Times New Roman", 20), fg="#e6e8eb", bg="#333333")
    top_title.pack(pady=10)

    def change():
        # This method will change the settings of the question which is displayed
        global ques_category, ques_difficulty, question_type, ques_category_selected, ques_difficulty_selected, \
            ques_type_selected, correct_option_index

        # If question is not loaded then we cannot make any changes
        if correct_option_index == -1:
            messagebox.showerror("Error", "Cannot apply changes util present question is loaded")
            return

        # Count variable will keep a count that settings are changed or not
        count = 0
        x = categories_var.get()
        if x != "Categories" and x != ques_category_selected:
            # Categories start with index 9 and categories in the category_list start with index 1
            ques_category = (8 + categories_list.index(x))
            ques_category_selected = x
            count += 1

        x = difficulty_var.get()
        if x != "Difficulty" and x != ques_difficulty_selected:
            if x == "Any Difficulty":
                ques_difficulty = ""
            else:
                ques_difficulty = x.lower()
            ques_difficulty_selected = x
            count += 1

        x = type_var.get()
        if x != "Type" and x != ques_type_selected:
            if x == "Multiple Choice":
                question_type = "multiple"
                btn3['state'] = NORMAL  # Multiple and boolean button settings
                btn4['state'] = NORMAL  # Multiple and boolean button settings
            else:
                question_type = "boolean"
                btn3['state'] = DISABLED  # Multiple and boolean button settings
                btn4['state'] = DISABLED  # Multiple and boolean button settings
            ques_type_selected = x
            count += 1

        if count > 0:
            # Loads a question
            threading.Thread(target=load_question, args=(1, )).start()
            question_display['state'] = NORMAL
            question_display.delete(1.0, END)
            question_display.insert(END, "Wait a moment...")
            question_display['state'] = DISABLED
            correct_option_index = -1

        # Closes the settings window
        top.destroy()

    def change_text_size():
        # Display text size will be changed by this method
        size = simpledialog.askinteger("Knowledge Check", "Enter Text Size (16-26): ")

        if size is None:
            return

        if size < 16 or size > 26:
            messagebox.showerror("Error", "Enter text sizes only in this range (16-26)")
        else:
            question_display['font'] = ("Times New Roman", size)
            prev_ans_display['font'] = ("Times New Roman", size-3)

    # Category option menu with its configurations, variable and list
    categories_list = ["Categories", "General Knowledge", "Entertainment: Books", "Entertainment: Film",
                       "Entertainment: Music", "Entertainment: Musicals & Theatres", "Entertainment: Television",
                       "Entertainment: Video Games", "Entertainment: Board Games", "Science & Nature",
                       "Science: Computers", "Science: Mathematics", "Mythology", "Sports", "Geography", "History",
                       "Politics", "Art", "Celebrities", "Animals", "Vehicles", "Entertainment: Comics",
                       "Science: Gadgets", "Entertainment: Japanese Anime & Manga",
                       "Entertainment: Cartoon & Animations"]
    categories_var = StringVar()
    categories_option_menu = ttk.OptionMenu(top, categories_var, *categories_list)
    categories_var.set(ques_category_selected)
    categories_option_menu.pack(pady=6)

    # Difficulty option menu with its configurations, variable and list
    difficulty_var = StringVar()
    difficulty_list = ["Difficulty", "Easy", "Medium", "Hard", "Any Difficulty"]
    difficulty_option_menu = ttk.OptionMenu(top, difficulty_var, *difficulty_list)
    difficulty_var.set(ques_difficulty_selected)
    difficulty_option_menu.pack(pady=6)

    # Type option menu with its configurations, variable and list
    type_var = StringVar()
    type_list = ["Type", "Multiple Choice", "True/False"]
    type_option_menu = ttk.OptionMenu(top, type_var, *type_list)
    type_var.set(ques_type_selected)
    type_option_menu.pack(pady=6)

    # Change text size button with its configuration
    change_text_btn = Button(top, fg="#e6e8eb", bg="#333333", text="Change Display Text Size", command=change_text_size)
    change_text_btn.pack(pady=6)

    # Sound check box with its configurations
    sound_check_box = Checkbutton(top, fg="#e6e8eb", bg="#333333", text=" Sound ", variable=sound_var, offvalue=False,
                                  selectcolor="black")
    sound_check_box.pack(pady=6)
    if sound_var.get():
        sound_check_box.select()
    else:
        sound_check_box.deselect()

    # Change button with its change command
    change_btn = Button(top, text="Apply Settings", fg="#e6e8eb", bg="#993e1c", command=change)
    change_btn.pack(padx=10, pady=26)


def helps():
    # This will open about us window
    messagebox.showinfo("Help", "Knowledge Check Is A Program Which Will Display Questions Related To Various "
                                "Categories.\n"
                                "Settings : You Can Turn Sound On Or Off, Change Text Size And You "
                                "Can Select (Category, Difficulty, Type) Of The Questions By Clicking On "
                                "The Settings Menu.\n"
                                "Selecting Options : You Can Either click On The Option Buttons (OR) 1, 2, 3, 4 or "
                                "A, B, C, D Keys To Select An Option.\n"
                                "Knowledge Check Needs Internet Connection.\n")


def about_us():
    # This will open about us window
    messagebox.showinfo("About Us", "Knowledge Check Version 1.0\nDeveloped By Nikhil")


# Title label
title_lbl = Label(root, font=("Times New Roman", 26, "bold"), text="Knowledge Check", fg="#e6e8eb", bg="#333333")
title_lbl.pack()


# Score label
score_lbl = Label(root, font=("Times New Roman", 16), text="Correct: 0 \t\t   Wrong: 0", fg="#e6e8eb", bg="#333333")
score_lbl.pack()


# Question display
question_display = Text(root, wrap="word", height=8, cursor="arrow", font=("Times New Roman", 16), fg="#e6e8eb",
                        bg="#333333")
question_display.insert(END, "Welcome...")
question_display.pack(padx=1, pady=4)
question_display['state'] = DISABLED

# Binding 1, 2, 3, 4 Keys
root.bind("<Key-1>", btn1_command)
root.bind("<Key-2>", btn2_command)
root.bind("<Key-3>", btn3_command)
root.bind("<Key-4>", btn4_command)

# Binding Small a, b, c, d Keys
root.bind("<a>", btn1_command)
root.bind("<b>", btn2_command)
root.bind("<c>", btn3_command)
root.bind("<d>", btn4_command)

# Binding Capital A, B, C, D Keys
root.bind("<A>", btn1_command)
root.bind("<B>", btn2_command)
root.bind("<C>", btn3_command)
root.bind("<D>", btn4_command)

# Previous answer display
prev_ans_display = Text(root, wrap="word", height=4, cursor="arrow", font=("Times New Roman", 13), fg="#e6e8eb",
                        bg="#333333")
prev_ans_display.pack(padx=1, pady=25)
prev_ans_display.insert(END, "Previous Question With Answer Will Be Displayed Here\n\nStart Answering...")
prev_ans_display['state'] = DISABLED

# Buttons panel
buttons_area = Frame(bg="#333333")
buttons_area.pack()

# Buttons
btn1 = ttk.Button(buttons_area, text="Option A", command=btn1_command)
btn1.grid(row=0, column=0, padx=10, pady=6)

btn2 = ttk.Button(buttons_area, text="Option B", command=btn2_command)
btn2.grid(row=0, column=1, padx=10, pady=6)

btn3 = ttk.Button(buttons_area, text="Option C", command=btn3_command)
btn3.grid(row=0, column=2, padx=10, pady=6)

btn4 = ttk.Button(buttons_area, text="Option D", command=btn4_command)
btn4.grid(row=0, column=3, padx=10, pady=6)


# Menu
menu = Menu(root)
root.config(menu=menu)

# Help menu
help_menu = Menu(menu, tearoff=0)
menu.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="Help", command=helps)

# Settings menu
settings_menu = Menu(menu, tearoff=0)
menu.add_cascade(label="Settings", menu=settings_menu)
settings_menu.add_command(label="Open Settings", command=settings)

# About us menu
about_menu = Menu(menu, tearoff=0)
menu.add_cascade(label="About", menu=about_menu)
about_menu.add_command(label="About Us", command=about_us)

# Loads a question and displays the question and loads next question argument 0 means no and 1 means display content
threading.Thread(target=load_question, args=(1, )).start()

# root.eval('tk::PlaceWindow . center')  # To place the window in center of screen
root.mainloop()
