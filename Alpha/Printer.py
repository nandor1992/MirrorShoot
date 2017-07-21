import os,subprocess
from PIL import Image

class Printer():
    def __init__(self):
        self.dir_path = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
        self.dir_path += "\Resource\Photo\\"
        printer=os.popen("wmic printer get name,portname").read()
        for line in printer.rsplit('\n'):
            if len(line)>=5:
                parts = line.rsplit()
                if parts[0]!="Name":
                    self.printer_name = " ".join(parts[:-1])
                    self.printer_port = parts[-1]
                    #print("Printer " +self.printer_name + " Port: "+self.printer_port)

    def printPhoto(self,name):
        img_file = Image.open(self.dir_path+name)
        img2=img_file.rotate(270,expand=True)
        img2.save(self.dir_path+"print.jpg")
        #os.system("mspaint /p "+self.dir_path+"print.jpg"+" /pt"+self.printer_name)
        command="print "+self.dir_path+"print.jpg" + " /d:"+self.printer_port
        print(command)
        os.system(command)

if __name__ == '__main__':
    p=Printer()
    p.printPhoto("show.jpg")