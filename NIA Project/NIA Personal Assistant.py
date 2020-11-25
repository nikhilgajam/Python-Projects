from tkinter import *
from tkinter import messagebox
from tkinter.font import Font
from tkinter import ttk
import wolframalpha
import webbrowser
import requests
import playsound
import threading
import wikipedia
import time

# Window

root = Tk()
root.title("NIA")
root.iconbitmap(True, "images/icon.ico")

# Search list

search_list = []
search_count = 0

# Operations


def ask_pressed(event=""):
    display.insert(END, "\n\n>>> " + str(ques.get()))
    display.yview(END)
    ask(str(ques.get()))


def ask(string):
    global search_list, search_count
    search_list.append(string)
    string = string.lower()

    if 'search' in string:
        string = string.replace("search", "")
        threading.Thread(target=sounds, args=("sounds/web.mp3", )).start()
        display.insert(END, "\n Redirecting your query to a web browser.")
        display.yview(END)
        webbrowser.open('https://www.google.com/search?q=' + string)

    elif 'hello' in string:
        display.insert(END, "\n " + "Hey. How can I help you?")

    elif 'hey' in string:
        display.insert(END, "\n " + "Hello. How can I help you?")

    elif 'nia' in string:
        display.insert(END, "\n " + "NIA is a Personal Assistant Created By Nikhil")
        
    elif string == '':
        display.insert(END, "\n " + "Try to type a question or name or anything.")
        threading.Thread(target=sounds, args=("sounds/type.mp3", )).start()

    elif 'date' in string:
        threading.Thread(target=sounds, args=("sounds/date.mp3", )).start()
        t = time.ctime()
        t = t[:10] + "," + t[19:]
        display.insert(END, "\n " + str(t))

    elif 'time in' in string:
        threading.Thread(target=sounds, args=("sounds/searching.mp3", )).start()
        client = wolframalpha.Client("U4L9E5-8RHX97YV24")
        res = client.query(string)
        data = next(res.results).text
        if data == '(no data available)' or data == '(data not available)':
            raise Exception
        display.insert(END, "\n " + str(data))
        display.yview(END)

    elif 'time' in string:
        threading.Thread(target=sounds, args=("sounds/time.mp3", )).start()
        t = time.ctime()
        change = int(t[11:13]) % 12
        temp = t[11:]
        temp = temp.replace(t[11:13], str(change), 1)
        t = t[0:11] + temp
        display.insert(END, "\n " + str(t))

    elif 'weather' in string:
        string = string.split(" ")
        try:
            city = string[string.index('in') + 1]
            if len(string) - 1 > string.index('in') + 2:
                city = string[string.index('in') + 1] + " " + string[string.index('in') + 2] + " " + string[string.index('in') + 3]
                print(city)
            elif len(string) - 1 > string.index('in') + 1:
                city = string[string.index('in') + 1] + " " + string[string.index('in') + 2]
        except Exception:
            display.insert(END, "\n " + "How To Get Weather Data: \nEx: Weather in city (or) What's the weather in hyderabad")
            display.yview(END)
            return
        try:
            url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=0c42f7f6b53b244c78a418f4f181282a&units=metric'.format(city)
            dat = requests.get(url)
            data = dat.json()
            temp = data['main']['temp']
            wind_speed = data['wind']['speed']
            country = data['sys']['country']
            place = data['name']
            humidity = data['main']['humidity']
            pressure = data['main']['pressure']
            min_temp = data['main']['temp_min']
            max_temp = data['main']['temp_max']
            latitude = data['coord']['lat']
            longitude = data['coord']['lon']
            description = data['weather'][0]['description']
            info = "City : {}\nCountry : {}\nTemperature : {}°C\nDescription : {}\nMinimum Temperature : {}°C\nMaximum Temperature : {}°C\nHumidity : {}%\nPressure : {} hpa\nWind Speed : {} m/s\nLatitude : {}\nLongitude : {}".format(place, country, temp, description, min_temp, max_temp, humidity, pressure, wind_speed, latitude, longitude)
            threading.Thread(target=sounds, args=("sounds/weather.mp3", )).start()
            display.insert(END, "\n " + str(info))
        except Exception:
            display.insert(END, "\n There's a problem with keyword or internet connection. Please retry.")
            display.yview(END)
            threading.Thread(target=sounds, args=("sounds/retry.mp3", )).start()

    else:
        # This will search the wolfram alpha if not found then searches on wikipedia after that searches on google
        threading.Thread(target=internet_search, args=(str(string), )).start()

    ques.delete(0, END)
    search_count = 0


def internet_search(string):
    try:
        threading.Thread(target=sounds, args=("sounds/searching.mp3", )).start()
        client = wolframalpha.Client("U4L9E5-8RHX97YV24")
        res = client.query(string)
        data = next(res.results).text
        if data == '(no data available)' or data == '(data not available)':
            raise Exception
        display.insert(END, "\n " + str(data))
        display.yview(END)
    except Exception:
        try:
            data = wikipedia.summary(string, sentences=3)
            display.insert(END, "\n " + str(data))
            display.insert(END, "\n\nIf this answer is not acceptable try placing 'search' in front of the query.\nEx: search Nikhil Tech")
            display.yview(END)
        except Exception:
            threading.Thread(target=sounds, args=("sounds/web.mp3", )).start()
            display.insert(END, "\n Redirecting your query to a web browser.")
            display.yview(END)
            webbrowser.open('https://www.google.com/search?q=' + string)


def search_track(event=""):
    global search_list, search_count
    print(search_count, search_list)
    try:
        ques.delete(0, END)
        search_count = search_count - 1
        ques.insert(0, search_list[search_count])
    except Exception:
        pass


def sounds(source):
    playsound.playsound(source)


def copy():
    display.clipboard_clear()
    display.clipboard_append(display.selection_get())


def select_all():
    display.tag_add(SEL, "1.0", END)
    display.mark_set(INSERT, 1.0)
    display.see(INSERT)


def helps():
    messagebox.showinfo("Help", "You Can Scroll The Display\nCheck internet error also refers to keyword error")


def about():
    messagebox.showinfo("About", "NIA is a personal assistant created by Nikhil")


def popup(event):
    popup_menu.post(event.x_root, event.y_root)  # Popup menu


# NIA Image

pic = PhotoImage(file="images/artificial-intelligence.png")

image = Label(image=pic)
image.pack()

# Text type

types = Font(family="Lucida Console")

# Data Display

display = Text(root, font=types, foreground="#dadce0", background="#35363a", undo=True, insertbackground="#dadce0", wrap="word")
display.bind("<Button-3>", popup)  # Popup Menu Binding
display.pack(fill=BOTH, expand=True)

box = Frame(root)
box.pack()

# Question Box

ques = Entry(box, font=types, width=80)
ques.bind("<Return>", ask_pressed)
ques.bind("<Up>", search_track)
ques.grid(row=0, column=0, padx=3)
ques.focus()

# Ask Button

ask_btn = ttk.Button(box, text="Ask", command=ask_pressed)
ask_btn.grid(row=0, column=1, padx=3, pady=6)

# Welcome string with sound

display.insert(END, ">>> Hey there. I'm NIA (Nikhil's Assistant). How can I help you?")
threading.Thread(target=sounds, args=("sounds/greeting.mp3", )).start()

# Popup Menu

popup_menu = Menu(root, tearoff=0)

popup_menu.add_command(label="Copy", command=copy)
popup_menu.add_separator()
popup_menu.add_command(label="Undo", command=display.edit_undo)
popup_menu.add_command(label="Redo", command=display.edit_redo)
popup_menu.add_separator()
popup_menu.add_command(label="Select All\t\t\t", command=select_all)
popup_menu.add_separator()
popup_menu.add_command(label="Help", command=helps)
popup_menu.add_separator()
popup_menu.add_command(label="About", command=about)

root.mainloop()
