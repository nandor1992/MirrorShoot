from PIL import Image
import os

class Editor():
    def __init__(self, name,relSize,emoji_width):
        self.name=name
        self.realSize=relSize
        self.eWidth=emoji_width
        self.base_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

    def update(self,name):
        self.name=name

    def addFrame(self,frame):
        cover_file = Image.open(frame)
        pic=Image.open(self.name)
        pic.paste(cover_file, (0, 0), cover_file)
        #pic.save(self.name[:-4]+"_edited.JPG")
        pic.save(self.name)

    def addEmojis(self,eName,eSize,ePosition):
        print(eName)
        print(eSize)
        print(ePosition)
        print(self.name)
        print(self.realSize)
        print(self.eWidth)
        pic = Image.open(self.name)
        width, height = pic.size
        print([width,height])
        ratio=width/self.realSize[0]
        for n in eName:
            emoji = Image.open(self.base_dir+"/Resource/Image/Emoji/"+eName[n])
            w,h=emoji.size
            print([w,h])
            r2=self.eWidth/w
            emoji = emoji.resize((int(ratio*w*r2*eSize[n]), int(r2*h*ratio*eSize[n])), Image.BICUBIC)
            pic.paste(emoji, (int((ePosition[n][0]-8)*ratio), int((ePosition[n][1]-24)*ratio)), emoji)
        pic.save(self.name)
        #pic.save(self.name[:-4] + "_edited.JPG")



if __name__ == '__main__':
    e=Editor("../Resource/Photo/DSC_0303.JPG",[1029, 1542],187.8)
    e.addEmojis({'0':"Angel_Halo_Emoji_Icon.png"},{'0':1.7},{'0':[300,-100]})
    #e.addFrame("../Resource/Image/Frames/frame.png")