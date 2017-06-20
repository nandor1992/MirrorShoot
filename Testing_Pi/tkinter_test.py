# import Image and the graphics package Tkinter
from Tkinter import *
from PIL import ImageTk, Image
import picamera

class Camera:

    def __init__(self):
        self.camera=picamera.PiCamera()
        self.camera.resolution=(1920,1080)
        
    def takePic(self):
        self.camera.capture("test_image.jpg")

class MainWindow():

    def __init__(self, main):

        # canvas for image
        self.main=main
        self.canvas = Canvas(main, width=1680, height=920)
        self.canvas.grid(row=0, column=0)
        main.attributes("-fullscreen", True)
        # images
        self.path="test_image.jpg"
        self.my_images=ImageTk.PhotoImage(Image.open(self.path))


        # set first image on canvas
        self.image_on_canvas = self.canvas.create_image(0, 0, anchor = NW, image = self.my_images)

        # button to change image
        self.button = Button(main, text="Change", command=self.onButton)
        self.button.grid(row=1, column=0)
        self.button = Button(main, text="Exit", command=self.onExit)
        self.button.grid(row=2, column=0)

    def initCam(self,c):
        self.camera=c

    def onExit(self):
        self.main.destroy()

    def onButton(self):

        c.takePic()
        self.my_images=ImageTk.PhotoImage(Image.open(self.path))
        # change image
        self.canvas.itemconfig(self.image_on_canvas, image = self.my_images)

c=Camera()
c.takePic()
root = Tk()
m=MainWindow(root)
m.initCam(c)
root.mainloop()
