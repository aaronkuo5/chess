from tkinter import * 
from PIL import Image,ImageTk  
root = Tk()  
root.title("display image")  
im=Image.open("images/p_white.png")  
photo=ImageTk.PhotoImage(im)  
# cv = Canvas(background="blue")  
# cv.pack(side='top', fill='both')  
# cv.create_image(10, 10, image=photo, anchor='nw')  

btn_column = Label(root, image = photo)
btn_column.grid(column=8, row=8)

a = Label(root, image = photo, height=200, width = 200)
a.grid(column=7, row=7)

c = Label(root, image = photo)
c.grid(column=6, row=6)

d = Label(root, image = photo)
d.grid(column=5, row=5)

e = Label(root, image = photo)
e.grid(column=4, row=4)

f = Label(root, image = photo)
f.grid(column=3, row=3)

g = Label(root, image = photo)
g.grid(column=2, row=2)

h = Label(root, image = photo)
h.grid(column=1, row=1)
root.mainloop()