from PIL import Image
import os

class Editor():
    def __init__(self, name):
        self.name=name
        self.orig=Image.open(name)
        self.base_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
        self.stat="Original"

    def addFrame(self,frame):
        cover_file = Image.open(frame)
        pic=self.orig.copy()
        pic.paste(cover_file, (0, 0), cover_file)
        pic.save(self.base_dir+"/Resource/Photo/show.jpg")
        self.stat = "Framed"
        return pic

    def removeFrame(self):
        self.orig.save(self.base_dir+"/Resource/Photo/show.jpg")
        self.stat = "Original"
        return self.orig



if __name__ == '__main__':
    e=Editor()
    #img =QPixmap("../Resource/Photo/DSC_0303.JPG")
    img=Image.open("../Resource/Photo/DSC_0303.JPG")
    ret_img=e.addFrame(img,"../Resource/Image/frame.png")