from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image, ImageDraw, ImageFont
import os

filename = ''
watermark_text = ''
new_file = ''
opacity = 255

# This is a test

def UploadAction():
    global filename
    filename = filedialog.askopenfilename()
    image = Image.open(filename)
    img = image.resize((500, 600))
    my_img = ImageTk.PhotoImage(img)

    image_display_box.configure(image=my_img)
    image_display_box.image = my_img

    entry.grid(column=0, row=2, columnspan=3)
    entry.grid_configure(pady=(5, 0))
    opacity_slider.grid(column=0, row=4)
    opacity_label.grid(column=0, row=5)
    font_size_spinner.grid(column=2, row=4)
    font_label.grid(column=2, row=5)
    button.grid(column=0, row=3, columnspan=3)
    button.config(text="Add Text", command=AddText)

    window.config(padx=10, pady=10)


def AddText():
    global watermark_text

    watermark_text = entry.get()

    entry.delete(0, END)
    entry.insert(END, string="New File Name")

    button.grid(column=0, row=3, columnspan=3)
    button.config(text="Save Image", command=SaveImage)    

def SaveImage():
    global new_file, font_size
    new_file_name = entry.get()
    file_path = os.path.split(filename)
    new_file = f"{file_path[0]}/{new_file_name}.png"

    with Image.open(filename).convert("RGBA") as base:
        txt = Image.new("RGBA", base.size, (255, 255, 255, 0))
        fnt = ImageFont.truetype("AGENCYR.TTF", int(font_size_spinner.get()))
        d = ImageDraw.Draw(txt)
        d.text((10, 10), watermark_text, font=fnt, fill=(255, 255, 255, opacity))
        out = Image.alpha_composite(base, txt)
        out.save(new_file)
    DisplayNewImage()

def DisplayNewImage():
    image = Image.open(new_file)
    img = image.resize((500, 600))
    my_img = ImageTk.PhotoImage(img)

    image_display_box.configure(image=my_img)
    image_display_box.image = my_img

    font_size_spinner.grid_forget()
    font_label.grid_forget()
    opacity_label.grid_forget()
    opacity_slider.grid_forget()
    entry.grid_forget()

    button.config(text="Add Text To Another Image", command=ResetApp)

def OpacitySelection(value):
    global opacity
    opacity = 255
    value = int(value) / 100
    opacity = round(opacity * value)

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
logo.grid(column=0, row=0, columnspan=3)

image_display_box = Label()
image_display_box.config(padx=20, pady=20, background="light gray")
image_display_box.grid(column=0, row=1, columnspan=3)

font_size_spinner = Spinbox(from_=10, to=500, width=5)
font_label = Label()
font_label.config(padx=20, pady=20, background="light gray", text="Font Size", wraplength=60)

opacity_slider = Scale(from_=1, to=100, command=OpacitySelection, background="light gray", orient=HORIZONTAL, highlightthickness=0)
opacity_slider.set(100)
opacity_label = Label()
opacity_label.config(padx=20, pady=20, background="light gray", text="Opacity Percentage", wraplength=60)

entry = Entry(width=50)
entry.insert(END, string="Text to Add")

button = Button(window, text='Open Image', command=UploadAction, width=50)
button.grid_configure(pady=(5, 20), padx=20)
button.grid(column=0, row=2, columnspan=3)

window.mainloop()