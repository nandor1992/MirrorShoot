import picamera
import time
from appJar import gui


class GUI:
    def __init__(self,camera):
        self.app=gui("Selfie Device")
        self.app.startLabelFrame("Image",0,0)
        self.app.addImage("simple","test_image.jpg")
        self.app.stopLabelFrame()
        self.app.addButtons(["Submit","Exit"] ,self.press, colspan=2)
        self.camerpya=camera
        
    def press(self, btnName):
        print("Button Pressed: "+btnName)
        if btnName=="Exit":
            quit()
        else:
            self.camera.takePic()
            self.changePicture()
        print("picture taken, now show")

    def changePicture(self):
        self.app.reloadImage("reloaded","test_image.jpg")

    def start(self):
        self.app.go()
        
class Camera:

    def __init__(self):
        self.camera=picamera.PiCamera()
        self.camera.resolution=(1024,768)
        
    def takePic(self):
        self.camera.capture("test_image.jpg")

if __name__=="__main__":
    print("Starting script")
    cam=Camera()
    g=GUI(cam)
    g.start()
