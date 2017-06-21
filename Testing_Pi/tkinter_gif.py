from tkinter import *
root = Tk()
frames=[]
i=0
try:
    while True:
        frames.append(PhotoImage(file='load.gif',format = 'gif -index '+str(i) ))
        i+=1
except:
    pass
def update(ind):
    try:
        frame = frames[ind]
        ind += 1
        label.configure(image=frame)
        root.after(100, update, ind)
    except IndexError:
        ind=0
        frame = frames[ind]
        ind += 1
        label.configure(image=frame)
        root.after(100, update, ind)
label = Label(root)
label.pack()
root.after(0, update, 0)
root.mainloop()
