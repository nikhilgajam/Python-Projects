from tkinter import *
from tkinter import messagebox
import threading

# Window
window = Tk()
window.title("Dictionary")
window.config(bg="#333333")

# Variables
dictionary = {}
keywords = []
keyword_pointer = 0

# Methods


def start(e=""):
    try:
        # Opening the dictionary.data, reading and storing the data in a dictionary
        p = open("dictionary.data", "r", encoding="utf-8")
        data = p.read()
        data = data.split("\n")

        for i in data:
            if i != "":
                x = i.split(" == ")
                dictionary[x[0]] = x[1]

        del dictionary['_Keyword_']   # Removing _Keyword_
        
        p.close()

    except Exception as e:
        # Showing the error message
        messagebox.showerror("Error", "dictionary.data not found it is needed for execution of this program.\n" + str(e))


def update_list(e=""):
    # This method will update the contents on the display when you type in the input_box
    global keyword_pointer
    
    inp = input_box.get()  # Getting the input data

    use_display()

    # input should not to be null string
    if inp != "":
        display.delete(1.0, END)
        keywords.clear()

        for i in dictionary.keys():
            # Searching all types of the given input
            if i.startswith(inp) or i.startswith(inp.lower()) or i.startswith(inp.title()) or i.startswith(inp.upper()):
                keywords.append(str(i))
    
        display.insert(INSERT, "\n".join(keywords))
        keyword_pointer = -1  # Setting the keyword_pointer to -1 when list gets updated
    
    else:
        # Clearing the screen and keywords list
        display.delete(1.0, END)
        keywords.clear()

    stop_using_display()


def get_meaning(e=""):
    # This method will show you meaning when you click search or hit enter key
    inp = input_box.get()  # Getting the input data

    count = 0  # If this counter value is four then it means answer not found
    ans = set()  # Using the set datatype to avoid duplicate data

    # Search all types of answer for the given keyword
    for i in [inp, inp.lower(), inp.title(), inp.upper()]:
        x = dictionary.get(i)

        if x is None:
            count += 1  # Increasing the count if answer not found
        else:
            ans.add("◀ " + i + " ▶ : ⇱\n⤷ " + x + "\n\n")   # adding to the set if answer found

    use_display()

    if count == 4:
        # Clearing the screen and showing not found message
        display.delete(1.0, END)
        display.insert(INSERT, "Requested word not found.")
    else:
        # Formatting the displaying answer with new line and arrow
        ans = "".join(ans)
        ans = ans.replace("||", "\n⤷ ")
        display.delete(1.0, END)
        display.insert(INSERT, ans)

    stop_using_display()


def arrow_selector(arrow):
    # This method is going to point arrow to the selected word on the display when up and down arrows are used
    global keyword_pointer

    # If input is a null string then do nothing
    if input_box.get() == "":
        return

    if arrow == "up":
        if keyword_pointer > 0:
            keyword_pointer -= 1
    else:
        if keyword_pointer < len(keywords)-1:
            keyword_pointer += 1

    use_display()

    # Making the pointer to point at the selected keyword when arrow up/down arrow keys are used
    pos = str(keyword_pointer+1) + ".0"   # Position string which will be pointing to selected word Ex: 1.0
    display.delete(1.0, END)
    display.insert(INSERT, "\n".join(keywords))
    display.insert(pos, " ➔ ")  # ➵  Adding the arrow to the selected word
    display.yview(pos)  

    input_box.delete(0, END)
    input_box.insert(0, keywords[keyword_pointer])

    stop_using_display()


def use_display():
    display.config(state=NORMAL)


def stop_using_display():
    display.config(state=DISABLED)


# Heading
heading = Label(window, text="Dictionary", font=("Times New Roman", 28), fg="#e6e8eb", bg="#333333")
heading.pack(expand=TRUE, fill=BOTH)

# Display
display = Text(window, font=("Times New Roman", 15), wrap="word", height=16, fg="#e6e8eb", bg="#333333")
display.pack(fill=X, expand=TRUE)
display.bind("<Button-1>", lambda e: input_box.focus())
display.insert(INSERT, "Welcome...\n\nType Any Word And Use Up/Down Arrow Keys To Navigate.\nYou Can Press Enter Key Or Search Button To Get The Meaning Of Your Query.\n\n\n\n\n\n\n\n\t\t\t\t\t\tOffline Dictionary Created By Nikhil")
stop_using_display()

# Input box
input_box = Entry(window, font=("Times New Roman", 13), bg="#e6e8eb")
window.bind("<Key>", update_list)
window.bind("<Return>", get_meaning)
window.bind("<Up>", lambda e: arrow_selector("up"))
window.bind("<Down>", lambda e: arrow_selector("down"))
input_box.pack(expand=TRUE, fill=X, padx=50, pady=10)
input_box.focus()

# Input button
input_btn = Button(window, text="Search", font=("Times New Roman",), command=get_meaning, fg="#e6e8eb", bg="#333333")
input_btn.pack(pady=3)

# Reading and storing the dictionary.data
start()

window.mainloop()
