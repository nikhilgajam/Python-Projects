from tkinter import *
from tkinter import filedialog, messagebox as tm
from PIL import ImageGrab
import time

# Command


def screen_shot():
    # Minimizes the window
    root.iconify()
    # Waits the computer
    time.sleep(1.2)
    # Takes Screenshot
    image = ImageGrab.grab()
    # Saving
    save_path = filedialog.asksaveasfilename(initialfile="Capture.png", defaultextension=".png",
                                             filetype=(("PNG", "*.png"), ("JPEG", "*.jpeg"), ("PDF", "*.pdf"),
                                                       ("BMP", "*.bmp")))
    # checks the path exists or not
    if save_path == "":
        root.state("normal")
        return
    # Saving the image
    image.save(save_path)
    root.state("normal")


def about():
    tm.showinfo("About Creator", "This code is written by Nikhil")


# Main

root = Tk()
root.iconbitmap(True, "images/win_icon.ico")
root.title("Screen Capture")
# Menu

menu = Menu(root)
root.config(menu=menu)

abt_menu = Menu(menu, tearoff=0)
menu.add_cascade(label="About", menu=abt_menu)
abt_menu.add_command(label="About Creator", command=about)

# Label

lbl = Label(root, text="Screen Capture", font="Pristina 46")
lbl.pack()

# Image
img = PhotoImage(file="images/btn.png")

# Button

btn = Button(root, image=img, command=screen_shot)  # we can keep border=0 to show only image
btn.pack()

root.mainloop()
