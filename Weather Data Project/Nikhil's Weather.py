from tkinter import *
from tkinter import ttk
from tkinter import messagebox as tm
import requests

root = Tk()
root.geometry("842x559")
root.resizable(0, 0)
root.title("Nikhil's Weather")
root.iconbitmap(True, 'images//icon.ico')

pic = PhotoImage(file="images/pic.png")
bg_image = Label(root, image=pic)
bg_image.pack(side=LEFT)


# Heading Label

lbl = Label(root, font="Courier", text="The Ultimate Nikhil's Weather", fg="white", bg="#093a56")
lbl.place(x=270, y=1)

# Commands


def weather(*args):
    try:
        city = ent.get()
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

        bottom.place(x=260, y=200)
        display = "City : {}\nCountry : {}\nTemperature : {}°C\nDescription : {}\nMinimum Temperature : {}°C\nMaximum Temperature : {}°C\nHumidity : {}%\nPressure : {} hpa\nWind Speed : {} m/s\nLatitude : {}\nLongitude : {}".format(place, country, temp, description, min_temp, max_temp, humidity, pressure, wind_speed, latitude, longitude)
        disp['text'] = display
        disp.pack()

    except:

        bottom.place(x=181, y=200)
        disp['text'] = "Cannot Retrieve The Information At This Moment"
        disp.pack()


def about_us():
    tm.showinfo("About Us", "This Is Developed By Nikhil")


def helps():
    bottom.place(x=3, y=200)
    disp['text'] = "Cannot Retrieve The Information Is Displayed Due To Misspelling Or Internet Problem"
    disp.pack()


# Menu

m = Menu(root)
root.config(menu=m)

am = Menu(m, tearoff=0)
m.add_cascade(label="About", menu=am)
am.add_command(label="About Us", command=about_us)
am.add_command(label="Help", command=helps)


# Top

top = Frame(root, bg="#156679", bd=10)
top.place(x=65, y=100)

ent = ttk.Entry(top, font="Courier", width=50)
ent.focus_set()
ent.bind("<Return>", weather)
ent.pack(side=LEFT, padx=15, pady=20)

btn = Button(top, text="Get Weather", command=weather, font="Courier", bg="white")
btn.pack(side=LEFT, padx=15, pady=20)

# Bottom

bottom = Frame(root)
bottom.place(x=270, y=200)

disp = Label(bottom, font="Courier", text="You Can Enter City, Place Or Pin Code To Get Weather Information", fg="white", bg="#0b476c")
bottom.place(x=100, y=200)
disp.pack()

root.mainloop()
