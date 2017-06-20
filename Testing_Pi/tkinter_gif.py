from Tkinter import *
import time
import os

root = Tk()

frames = [PhotoImage(file='test.gif',format = 'gif -index %i' %(i)) for i in range(10)]

def update(ind):

    frame = frames[ind]
    ind += 1
    label.configure(image=frame)
    root.after(100, update, ind)
label = Label(root)
label.pack()
root.after(0, update, 0)
root.mainloop()
