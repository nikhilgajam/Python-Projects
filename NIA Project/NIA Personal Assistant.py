from tkinter import *
from tkinter import messagebox
from datetime import datetime
from tkinter.font import Font
from tkinter import ttk
from gtts import gTTS
import urllib.request
import wolframalpha
import webbrowser
import playsound
import threading
import wikipedia
import requests
import calendar
import shutil
import time
import os

# Window

root = Tk()
root.title("NIA")
root.iconbitmap(True, "images/icon.ico")

# Search list

search_list = []
search_count = 0

# Internet check variable

check = None


# Operations


def ask_pressed(event=""):
    display['state'] = NORMAL
    display.insert(END, "\n\n>>> " + str(ques.get()))
    display.yview(END)
    ask(str(ques.get()))
    display['state'] = DISABLED
    # print(threading.active_count())


def ask(string):
    global search_list, search_count, check

    # Search record
    search_list.append(string)

    # Cleaning the input string
    string = string.strip().lower()

    display['state'] = NORMAL
    ques.focus()

    if string.startswith("search"):
        string = string.replace("search", "")
        threading.Thread(target=sounds, args=("sounds/web.mp3",)).start()
        display.insert(END, "\n Redirecting your query to a web browser.")
        display.yview(END)
        webbrowser.open('https://www.google.com/search?q=' + string)

    elif string.endswith('hello') or string.endswith('hello nia'):
        display.insert(END, "\n " + "Hey. How can I help you?")

    elif string.startswith('hey') or string.endswith('hey nia'):
        display.insert(END, "\n " + "Hello. How can I help you?")

    elif string.startswith('hi') or string.endswith('hi nia'):
        display.insert(END, "\n " + "Hello. How can I help you?")

    elif string.startswith('nia'):
        display.insert(END, "\n " + "NIA is a Personal Assistant Created By Nikhil")

    elif string.endswith('your name') or string.endswith('your name?'):
        display.insert(END, "\n " + "I am NIA.")
        threading.Thread(target=sounds, args=("sounds/nia.mp3",)).start()

    elif string.startswith('open'):
        temp = string.replace("open ", "")
        try:
            os.startfile(temp)
            del temp
            display.insert(END, "\n " + "Done.")
        except Exception:
            threading.Thread(target=internet_search, args=(str(string),)).start()

    elif string == '':
        display.insert(END, "\n " + "Try to type a question or name or anything.")
        threading.Thread(target=sounds, args=("sounds/type.mp3",)).start()

    elif string.startswith('date') or string.endswith('date'):
        threading.Thread(target=sounds, args=("sounds/date.mp3",)).start()
        t = time.ctime()
        t = t[:10] + "," + t[19:]
        display.insert(END, "\n " + str(t))

    elif 'time in' in string:
        threading.Thread(target=internet_search, args=(str(string),)).start()

    elif string.endswith('time') or string.endswith('time now'):
        threading.Thread(target=sounds, args=("sounds/time.mp3",)).start()
        t = time.ctime()
        change = int(t[11:13]) % 12
        temp = t[11:]
        temp = temp.replace(t[11:13], str(change), 1)
        t = t[0:11] + temp
        display.insert(END, "\n " + str(t))

    elif string == 'calendar':
        t = time.ctime()
        t = t[:10] + "," + t[19:]
        months = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10,
                  "Nov": 11, "Dec": 12}
        display.insert(END, "\n" + calendar.month(int(t[-4:]), int(months[t[4:7].strip()])))
        display.insert(END, "\n" + str(t))
        display.yview(END)

    elif 'weather' in string:
        if check is None:
            internet_issue()
            return

        threading.Thread(target=weather_data, args=(string,)).start()

    elif string == 'help':
        display.insert(END, "\n" + " weather in <city-name> - Displays weather data in a particular city\n"
                                   " search <keyword>       - Redirects your query to a web browser\n"
                                   " open <app or file>     - Opens a specific app/file or website\n"
                                   " calendar               - Displays this month's calendar\n"
                                   " date                   - Displays today's date\n"
                                   " time                   - Displays time\n\n"
                                   " Any string which doesn't have any above command is taken as a Search Query.")
        display.yview(END)

    else:
        display['state'] = DISABLED
        # This will search the wolfram alpha if not found then searches on wikipedia after that searches on google
        threading.Thread(target=internet_search, args=(str(string),)).start()

    ques.delete(0, END)
    search_count = 0
    display['state'] = DISABLED


def internet_search(string):
    if check is None:
        internet_issue()
        return

    try:
        # Searches on wolfram alpha
        threading.Thread(target=sounds, args=("sounds/searching.mp3",)).start()
        client = wolframalpha.Client("U4L9E5-8RHX97YV24")
        res = client.query(str(string))
        data = next(res.results).text
        if data == '(no data available)' or data == '(data not available)':
            # If the answer is not found an exception is raised
            raise Exception
        display['state'] = NORMAL
        display.insert(END, "\n " + str(data))
        display.yview(END)
        display['state'] = DISABLED
        threading.Thread(target=string_to_speech, args=(str(data), )).start()
    except Exception:
        try:
            # Then searches on wikipedia
            data = wikipedia.summary(str(string), sentences=3)
            display['state'] = NORMAL
            display.insert(END, "\n " + str(data))
            display.insert(END, "\n\nIf this answer is not acceptable try placing 'search' in front of the query.\nEx: search Nikhil Tech")
            display.yview(END)
            display['state'] = DISABLED
            threading.Thread(target=sounds, args=("sounds/data.mp3",)).start()
        except Exception:
            # When answer is not found on wikipedia then it will open a web browser and searches on google
            threading.Thread(target=sounds, args=("sounds/web.mp3",)).start()
            display['state'] = NORMAL
            display.insert(END, "\n Redirecting your query to a web browser.")
            display.yview(END)
            display['state'] = DISABLED
            webbrowser.open('https://www.google.com/search?q=' + str(string))

    threading.Thread(target=internet_check, args=()).start()


def weather_data(string):
    city = ""
    display['state'] = NORMAL
    # Cleaning the string to get weather data or weather help
    if string.startswith('weather in '):
        city = string.replace("weather in ", "")
    elif string.startswith("what's the weather"):
        city = string.replace("what's the weather in ", "")
    elif string.startswith("whats the weather"):
        city = string.replace("whats the weather in ", "")
    elif string.startswith("how's the weather"):
        city = string.replace("how's the weather in ", "")
    elif string.startswith("hows the weather"):
        city = string.replace("hows the weather in ", "")
    elif string.startswith("weather help"):
        display.insert(END,
                       "\n " + "How To Get Weather Data: \nEx: Weather in city (or) What's the weather in hyderabad (or) How's the weather in hyderabad")
        display.yview(END)
        return

    city = city.strip()

    try:
        # Weather data program
        url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=0c42f7f6b53b244c78a418f4f181282a&units=metric'.format(
            city)
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
        info = "City : {}\nCountry : {}\nTemperature : {}°C\nDescription : {}\nMinimum Temperature : {}°C\nMaximum Temperature : {}°C\nHumidity : {}%\nPressure : {} hpa\nWind Speed : {} m/s\nLatitude : {}\nLongitude : {}".format(
            place, country, temp, description, min_temp, max_temp, humidity, pressure, wind_speed, latitude, longitude)
        threading.Thread(target=sounds, args=("sounds/weather.mp3",)).start()
        display.insert(END, "\n " + str(info))
        display.yview(END)

    except Exception:
        # When weather data is not found then it searches on internet
        threading.Thread(target=internet_search, args=(string,)).start()


def internet_check():
    global check

    try:
        urllib.request.urlopen("https://google.com")
        check = True
    except Exception:
        check = None


def internet_issue():
    display['state'] = NORMAL
    display.insert(END, "\n There's a problem with internet connection. Please retry.")
    display.yview(END)
    display['state'] = DISABLED
    threading.Thread(target=sounds, args=("sounds/retry.mp3",)).start()
    threading.Thread(target=internet_check, args=()).start()


def search_track(event=""):
    global search_list, search_count

    # When up arrow is pressed then this function is triggered and previous search strings are displayed

    try:
        ques.delete(0, END)
        search_count = search_count - 1
        ques.insert(0, search_list[search_count])
    except Exception:
        pass


def string_to_speech(string):
    mp3 = gTTS(str(string))
    string = search_list[-1].replace("*", "").replace("\\", "").replace("/", "").replace(":", "").replace("<", "").replace(">", "").replace("|", "")
    mp3.save("sounds/temp/" + str(string) + str(search_list.count(string)) + ".mp3")
    sounds("sounds/temp/" + str(string) + str(search_list.count(string)) + ".mp3")


def close():
    try:
        shutil.rmtree("sounds/temp")
    except Exception:
        pass

    root.destroy()


def sounds(source):
    playsound.playsound(source)


def copy():
    display.tag_add(SEL, "1.0", END)
    display.mark_set(INSERT, 1.0)
    display.see(INSERT)
    display.clipboard_clear()
    display.clipboard_append(display.selection_get())


def clicked(event=""):
    ques.focus()


def helps():
    ques.insert(0, "help")
    ask_pressed()
    messagebox.showinfo("Help", "You Can Scroll The Display")


def about():
    messagebox.showinfo("About", "NIA is a personal assistant created by Nikhil")
    webbrowser.open("https://youtube.com/NikhilTech")


def popup(event):
    popup_menu.post(event.x_root, event.y_root)  # Popup menu


# NIA Image

pic = PhotoImage(file="images/artificial-intelligence.png")

image = Label(image=pic)
image.pack()

# Text type

types = Font(family="Lucida Console")

# Data Display

display = Text(root, font=types, foreground="#dadce0", background="#35363a", undo=True, insertbackground="#dadce0", wrap="word", cursor="arrow")
display.bind("<Button-3>", popup)  # Popup Menu Binding
display.bind_all("<Button-1>", clicked)
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

if 5 <= int(datetime.today().hour) < 12:
    display.insert(END, ">>> Good Morning. I'm NIA (Nikhil's Assistant). How can I help you?")
    threading.Thread(target=sounds, args=("sounds/greetings/morning.mp3",)).start()
elif 12 <= int(datetime.today().hour) <= 16:
    display.insert(END, ">>> Good Afternoon. I'm NIA (Nikhil's Assistant). How can I help you?")
    threading.Thread(target=sounds, args=("sounds/greetings/afternoon.mp3",)).start()
elif 17 <= int(datetime.today().hour) < 24:
    display.insert(END, ">>> Good Evening. I'm NIA (Nikhil's Assistant). How can I help you?")
    threading.Thread(target=sounds, args=("sounds/greetings/evening.mp3",)).start()
else:
    display.insert(END, ">>> Hey There. I'm NIA (Nikhil's Assistant). How can I help you?")
    threading.Thread(target=sounds, args=("sounds/greetings/greeting.mp3",)).start()
    
# Stops the user to type on the display

display['state'] = DISABLED

# Creating temp directory

if os.path.isdir("sounds/temp"):
    shutil.rmtree("sounds/temp")

os.mkdir("sounds/temp")

# Internet Check

threading.Thread(target=internet_check, args=()).start()

# Popup Menu

popup_menu = Menu(root, tearoff=0)

popup_menu.add_command(label="Copy Data", command=copy)
popup_menu.add_separator()
popup_menu.add_command(label="Help", command=helps)
popup_menu.add_separator()
popup_menu.add_command(label="About", command=about)

root.protocol("WM_DELETE_WINDOW", close)
root.mainloop()
