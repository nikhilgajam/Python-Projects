from tkinter import *
from tkinter import filedialog
from tkinter import messagebox as tm
from PIL import Image
import PIL
import os
import webbrowser

root = Tk()
root.title("Image Compressor")
root.iconbitmap(True, "images/icon.ico")
root.config(bg="#333333")
root.resizable(0, 0)


needed_width = 1080

existing_dir = ""
new_dir = ""
count = 0


# Commands


def compress_image(exist_dir, new_p_dir, width):
    global existing_dir, new_dir
    try:
        if existing_dir == "":
            tm.showerror("Error", "Select Source Directory")
            stat['text'] = "Select Correct Source Directory"
            return

        if new_dir == "":
            tm.showerror("Error", "Select Destination Directory")
            stat['text'] = "Select Destination Directory"
            return

        img = Image.open(exist_dir)
        w_percent = (width/float(img.size[0]))
        h_size = int((float(img.size[1])*float(w_percent)))
        img = img.resize((width, h_size), PIL.Image.ANTIALIAS)

        if r_var.get() == 1:
            base_name = os.path.basename(exist_dir).split(".")
            base_name = base_name[0] + " (Compressed)" + "." + base_name[1]
            img.save(new_p_dir+"/"+base_name)
        elif r_var.get() == 2:
            img.save(new_p_dir)

        if count == 0:
            stat['text'] = "Compressed Successfully"
            existing_dir = ""
            new_dir = ""

    except PIL.UnidentifiedImageError:

        tm.showerror("Error", "Unidentified Image")
    except:

        tm.showerror("Error", "Select Correct Source & Destination Directories")
        stat['text'] = "Select Correct Source & Destination Directories"


def multiple_compress(exist_dir, new_p_dir, width):
    global existing_dir, new_dir, count

    try:
        pics = os.listdir(existing_dir)
        number = len(pics)
        stat['text'] = str(number) + " Images Are There In Source Directory"

        if existing_dir == "":
            tm.showerror("Error", "Select Source Directory")
            return

        if new_dir == "":
            tm.showerror("Error", "Select Destination Directory")
            return

        ask = tm.askyesno("Image Compressor",
                          str(number) + " Images Are There In Source Directory\n\nSource Directory : " + existing_dir
                          + "\nDestination Directory : " + new_dir + "\n\nDo You Want To Compress?")

        if ask != TRUE:
            stat['text'] = "OK"
            return

        for pic in pics:
            count += 1
            base_name = pic.split(".")
            base_name = base_name[0] + " (Compressed)" + "." + base_name[1]
            exist_dir = existing_dir + "/" + pic
            new_p_dir = new_dir + "/" + base_name
            compress_image(exist_dir, new_p_dir, width)

        stat['text'] = str(count) + " Images Compressed Successfully"
        existing_dir = ""
        new_dir = ""

    except:
        tm.showerror("Error", "Select Correct Source & Destination Directories")
        stat['text'] = "Select Correct Source & Destination Directories"


def single_multiple_pics():
    global needed_width, existing_dir, new_dir, count
    try:
        needed_width = int(ent.get())
    except ValueError:
        tm.showerror("Value Error", "Enter Only Numbers In Quality Box")

    compress_btn.config(cursor="watch")

    if r_var.get() == 1:
        compress_image(existing_dir, new_dir, needed_width)
    else:
        multiple_compress(existing_dir, new_dir, needed_width)

    compress_btn.config(cursor="arrow")

    count = 0


def quality_set():
    if q_var.get() == 1:
        ent.delete(0, END)
        ent.insert(END, "600")
    elif q_var.get() == 2:
        ent.delete(0, END)
        ent.insert(END, "1080")
    elif q_var.get() == 3:
        ent.delete(0, END)
        ent.insert(END, "1920")


def update_radio_btn(event=""):
    if ent.get() != "600" or ent.get() != "1080" or ent.get() != "1920":
        low.deselect()
        normal.deselect()
        high.deselect()


def sources_btn():
    global existing_dir
    if r_var.get() == 1:
        existing_dir = filedialog.askopenfilename()
    else:
        existing_dir = filedialog.askdirectory()

    if existing_dir != "":
        stat['text'] = "Source Directory Selected"


def destinations_btn():
    global new_dir
    new_dir = filedialog.askdirectory()

    if new_dir != "":
        stat['text'] = "Destination Directory Selected"


class HoverButton(Button):
    def __init__(self, master, **kw):
        Button.__init__(self, master=master, **kw)
        self.defaultBackground = self["background"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, event=""):
        self['background'] = self['activebackground']

    def on_leave(self, event=""):
        self['background'] = self.defaultBackground


def helps():
    top = Toplevel()
    top.title("About Image Compressor")
    top.resizable(0, 0)
    top.attributes("-toolwindow", 1)
    top.configure(bg="#333333")
    title = Label(top, text="Help", font="Pristina 40 underline", foreground="#e6e8eb", background="#333333")
    title.pack()
    about_lbl = Label(top, justify=LEFT, foreground="#e6e8eb", background="#333333", font="Verdana 12")
    about_lbl.configure(text="1. Select Single Image Or Multiple Images Radio Button\n2. Select Source And Destination "
                             "Directories\n3. Select Quality Mentioned As Radio Buttons Or Enter Desired Width\n"
                             "4. Click Compress To Start Compression\n\nAll The Compression Details Will Be Displayed "
                             "On The Status Bar\n\n\t          Thanks for Using Image Compressor")
    about_lbl.pack()
    about_lbl.focus_set()
    about_btn = HoverButton(top, text="   OK   ", fg="#e6e8eb", bg="#333333", activebackground="gray",
                            command=top.destroy)
    about_btn.pack()
    top.mainloop()


def abouts():
    webbrowser.open("https://youtube.com/nikhiltech")
    tm.showinfo("About Us", "This Code Is Written By Nikhil")


def about_compressor():
    top = Toplevel()
    top.title("About Image Compressor")
    top.attributes("-toolwindow", 1)
    top.config(bg="#333333")
    top.resizable(0, 0)
    title = Label(top, text="Image Compressor", font="Pristina 40 underline", foreground="#e6e8eb",
                  background="#333333")
    title.pack()
    about_lbl = Label(top, text="\nVersion : 1\nDeveloper : Nikhil\nOpen Source Image Compressor", justify=LEFT,
                      font="Verdana 12", foreground="#e6e8eb", background="#333333")
    about_lbl.focus_set()
    about_lbl.pack()
    about_btn = HoverButton(top, text="   OK   ", fg="#e6e8eb", bg="#333333", activebackground="gray",
                            command=top.destroy)
    about_btn.pack()
    top.mainloop()


# Menu


menu = Menu(root)
root.config(menu=menu)

about = Menu(menu, tearoff=0)
menu.add_cascade(label="Help", menu=about)
about.add_command(label="Help", command=helps)
about.add_command(label="About Creator", command=abouts)
about.add_command(label="About Image Compressor", command=about_compressor)


# Heading

r_var = IntVar()
q_var = IntVar()

head = Label(root, text="Image Compressor", font="Pristina 40", fg="#e6e8eb", bg="#333333")
head.pack(side=TOP, fill=BOTH)

# Buttons

source_image = PhotoImage(file="images\\source.png")
destination_image = PhotoImage(file="images\\destn.png")

btn = Frame(root, bg="#333333")
btn.pack(fill=BOTH)

source_btn = HoverButton(btn, text="Source", image=source_image, bg="#333333", command=sources_btn,
                         activebackground="gray")
source_btn.grid(row=0, column=0, padx=60, pady=1)
s = Label(btn, text="Source", fg="white", bg="#333333")
s.grid(row=1, column=0, padx=57)

destination_btn = HoverButton(btn, text="Destination", image=destination_image, bg="#333333", command=destinations_btn,
                              activebackground="gray")
destination_btn.grid(row=0, column=1, padx=50, pady=1)
d = Label(btn, text="Destination", fg="white", bg="#333333")
d.grid(row=1, column=1, padx=50)

# Pictures Heading

pictures = Label(root, text="Pictures", fg="#e6e8eb", bg="gray")
pictures.pack(fill=X)

# Radio buttons

single_multiple = Frame(root, bg="#333333")
single_multiple.pack(fill=BOTH)

single = Radiobutton(single_multiple, bg="#333333", activebackground="#333333", variable=r_var, value=1)
single.grid(row=0, column=0)
single.select()
sl = Label(single_multiple, text="Single Image", fg="#e6e8eb", bg="#333333")
sl.grid(row=1, column=0, padx=57)

multiple = Radiobutton(single_multiple, bg="#333333", activebackground="#333333", variable=r_var, value=2)
multiple.grid(row=0, column=1)
ml = Label(single_multiple, text="Multiple Images", fg="#e6e8eb", bg="#333333")
ml.grid(row=1, column=1, padx=50)

# Quality Heading

pictures = Label(root, text="Quality", fg="#e6e8eb", bg="gray")
pictures.pack(fill=X)

# Entry

space = Label(root, text="Enter The Image Width Below Or Select Any Button", fg="#e6e8eb", bg="#333333")
space.pack(fill=X)

ent = Entry(root, width=40, fg="#e6e8eb", bg="#993e1c", justify=CENTER)
ent.bind("<Key>", update_radio_btn)
ent.insert(0, "1080")
ent.pack()

quality = Frame(root, bg="#333333")
quality.pack()

# Quality Radio Buttons

low = Radiobutton(quality, bg="#333333", activebackground="#333333", variable=q_var, value=1, command=quality_set)
low.invoke()
low.grid(row=0, column=0, padx=40)
lw = Label(quality, text="Low", fg="#e6e8eb", bg="#333333")
lw.grid(row=1, column=0)

normal = Radiobutton(quality, bg="#333333", activebackground="#333333", variable=q_var, value=2, command=quality_set)
normal.invoke()
normal.grid(row=0, column=1, padx=40)
nl = Label(quality, text="Normal", fg="#e6e8eb", bg="#333333")
nl.grid(row=1, column=1)

high = Radiobutton(quality, bg="#333333", activebackground="#333333", variable=q_var, value=3, command=quality_set)
high.invoke()
high.select()
high.grid(row=0, column=2, padx=40)
hh = Label(quality, text="High", fg="#e6e8eb", bg="#333333")
hh.grid(row=1, column=2)

# Compress Heading

comp_t = Label(root, text="Compress", fg="#e6e8eb", bg="gray")
comp_t.pack(fill=X)

comp = Frame(root, bg="#333333")
comp.pack(anchor=S)

compress_pic = PhotoImage(file="images\\compress.png")
compress_btn = HoverButton(comp, image=compress_pic, bg="#333333", command=single_multiple_pics,
                           activebackground="gray")
compress_btn.pack()

stat = Label(root, text="Welcome To Image Compressor", fg="#e6e8eb", bg="gray", bd=5, relief=SUNKEN)
stat.pack(fill=X, side=BOTTOM, anchor=S)

root.mainloop()
