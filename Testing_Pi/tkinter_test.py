# import Image and the graphics package Tkinter
from tkinter import *
from PIL import ImageTk, Image
import time

class Camera:

    def __init__(self):
        pass
        #self.camera=picamera.PiCamera()
       # self.camera.resolution=(1920,1080)

    def takePic(self):
        pass
        #self.camera.capture("test_image.jpg")

class MainWindow():

    def __init__(self, main):
        self.stop = False
        # canvas for image
        self.main=main
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        self.canvas = Canvas(main, width=screen_width, height=screen_height,bd=0, highlightthickness=0, relief='ridge')
        self.canvas.grid(row=0, column=0)
        self.canvas.configure(background='black')
        main.configure(background='black')
        main.attributes("-fullscreen", True)
        # images
        self.path='test_image.jpg'
        image = Image.open('black.png')
        image = image.resize((screen_width,screen_height), Image.ANTIALIAS)  # The (250, 250) is (height, width)
        self.my_images=ImageTk.PhotoImage(image)
        self.image_on_canvas = self.canvas.create_image(screen_width/2,
                                                        screen_height/2, anchor=CENTER,
                                                        image=self.my_images)
        # set first image on canvas
        #Loader
        self.frames=[]
        i = 0
        try:
            while True:
                image = Image.open('load.gif')
                image.seek(i)
                im=image.copy()
                im = im.resize((200, 200), Image.BILINEAR)  # The (250, 250) is (height, width)
                self.frames.append(ImageTk.PhotoImage(im))
                i += 1
        except:
            pass
        # button to change image
        self.button = Button(main, text="Change", command=self.onButton,bd=0, highlightthickness=0, relief='ridge')
        image = Image.open("photo.png")
        image = image.resize((150,150), Image.ANTIALIAS)  # The (250, 250) is (height, width)
        self.imgb1=ImageTk.PhotoImage(image)
        self.button.config(image=self.imgb1)
        self.button.place(x=screen_width/2-200, y=screen_height/2+200, anchor=CENTER)
        self.button2 = Button(main, text="Exit", command=self.onExit,bd=0, highlightthickness=0, relief='ridge')
        image = Image.open("off.png")
        image = image.resize((150,150), Image.ANTIALIAS)  # The (250, 250) is (height, width)
        self.imgb2=ImageTk.PhotoImage(image)
        self.button2.config(image=self.imgb2)
        self.button2.place(x=screen_width/2+200, y=screen_height/2+200, anchor=CENTER)


    def initCam(self,c):
        self.camera=c

    def onExit(self):
        self.main.destroy()

    def update(self,ind):
        if time.time()-self.started<2:
            try:
                frame = self.frames[ind]
                ind += 1
                self.canvas.itemconfig(self.image_on_canvas2, image=frame)
                root.after(100, self.update, ind)
            except IndexError:
                ind = 0
                frame = self.frames[ind]
                ind += 1
                self.canvas.itemconfig(self.image_on_canvas2, image=frame)
                root.after(100, self.update, ind)
        else:
            self.canvas.delete(self.image_on_canvas2)
            self.displayNewImg()

    def onButton(self):
        self.wheel()
        c.takePic()

    def displayNewImg(self):
        image = Image.open(self.path)
        image = image.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.ANTIALIAS)  # The (250, 250) is (height, width)
        self.my_images = ImageTk.PhotoImage(image)
        # change image
        self.canvas.itemconfig(self.image_on_canvas, image = self.my_images)

    def wheel(self):
        self.image_on_canvas2 = self.canvas.create_image(self.canvas.winfo_width()/2, self.canvas.winfo_height()/2+50, anchor=CENTER, image=self.frames[0])
        self.main.after(0, self.update, 0)
        self.started=time.time()

    def motion(self,event):
        w=self.main.winfo_screenwidth()/2
        h=self.main.winfo_screenheight()/2
        x = self.main.winfo_pointerx() - self.main.winfo_rootx()
        y = self.main.winfo_pointery() - self.main.winfo_rooty()
        if x>=w-200-75 and x<=w-200+75 and y<=h+200+150 and y>=h+200-150:
            print("Photo")
        if x>=w+200-75 and x<=w+200+75 and y<=h+200+150 and y>=h+200-150:
            print("Exit")


c=Camera()
c.takePic()
root = Tk()
m=MainWindow(root)
m.initCam(c)
root.bind('<Button-1>', m.motion)
root.mainloop()
