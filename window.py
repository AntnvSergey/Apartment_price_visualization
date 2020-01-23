from tkinter import *
from tkinter.ttk import Combobox
from PIL import ImageTk
from imutils import paths


def show_label(label, image):
    label['image'] = image
    label.pack(side='left')
    label.update()


def callback(event):
    image_list = list(paths.list_images("./"+combo.get()))
    img1 = ImageTk.PhotoImage(file=image_list[0])
    img2 = ImageTk.PhotoImage(file=image_list[1])
    show_label(label1, img1)
    show_label(label2, img2)
    window.mainloop()


window = Tk()
window.title("Main window")
window.geometry('1400x600')
histogram1 = ImageTk.PhotoImage(file="./St.Petersburg/total_price.png")
histogram2 = ImageTk.PhotoImage(file="./St.Petersburg/area.png")
text = Label(window, text="Выбирите город:")
text.place(x=1285, y=250)
label1 = Label(window)
label2 = Label(window)
show_label(label1, histogram1)
show_label(label2, histogram2)
combo = Combobox(window)
combo['values'] = ("St.Petersburg", "Moscow", "Ekaterinburg")
combo.pack(side='left')
combo.current(0)
combo.bind("<<ComboboxSelected>>", callback)

window.mainloop()
