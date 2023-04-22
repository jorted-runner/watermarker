from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image, ImageDraw, ImageFont
import os

filename = ''
watermark_text = ''
new_file = ''

def UploadAction():
    global filename
    filename = filedialog.askopenfilename()
    image = Image.open(filename)
    img = image.resize((500, 600))
    my_img = ImageTk.PhotoImage(img)

    my_label.configure(image=my_img)
    my_label.image = my_img

    entry.grid(column=1, row=2)
    entry.grid_configure(pady=(5, 0))
    
    button.grid(column=1, row=3)
    button.config(text="Add Text", command=AddText)

    window.config(padx=10, pady=10)


def AddText():
    global watermark_text

    watermark_text = entry.get()

    entry.delete(0, END)
    entry.insert(END, string="New File Name")

    button.grid(column=1, row=3)
    button.config(text="Save Image", command=SaveImage)
    

def SaveImage():
    global new_file
    new_file_name = entry.get()
    file_path = os.path.split(filename)
    new_file = f"{file_path[0]}/{new_file_name}.png"

    with Image.open(filename).convert("RGBA") as base:
        txt = Image.new("RGBA", base.size, (255, 255, 255, 0))
        fnt = ImageFont.truetype("AGENCYR.TTF", 80)
        d = ImageDraw.Draw(txt)
        d.text((10, 10), watermark_text, font=fnt, fill=(255, 255, 255, 128))
        out = Image.alpha_composite(base, txt)
        out.save(new_file)
    DisplayNewImage()

def DisplayNewImage():
    image = Image.open(new_file)
    img = image.resize((500, 600))
    my_img = ImageTk.PhotoImage(img)

    my_label.configure(image=my_img)
    my_label.image = my_img

    entry.grid_forget()

    button.config(text="Add Text To Another Image", command=ResetApp)

def ResetApp():
    entry.delete(0, END)
    entry.insert(END, string="Text to Add")
    UploadAction()

window = Tk()
window.title("WaterMarker")
window.config(background="light gray")

logo = Label()
logo_image = Image.open("WaterMarker.png")
display_logo = ImageTk.PhotoImage(logo_image)
logo.config(background="light gray")
logo.configure(image=display_logo)
logo.image = display_logo
logo.grid(column=1, row=0)

my_label = Label()
my_label.config(padx=20, pady=20, background="light gray")
my_label.grid(column=1, row=1)

entry = Entry(width=50)
entry.insert(END, string="Text to Add")

button = Button(window, text='Open Image', command=UploadAction, width=50)
button.grid_configure(pady=(5, 20), padx=20)
button.grid(column=1, row=2)

window.mainloop()