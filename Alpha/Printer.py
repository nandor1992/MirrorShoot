import os,subprocess
from PIL import Image
import time

class Printer():
    def __init__(self):
        self.dir_path = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
        self.dir_path += "\Resource\Photo\\"
        printer=os.popen("wmic printer get name,portname").read()
        for line in printer.rsplit('\n'):
            if len(line)>=5:
                parts = line.rsplit()
                if parts[0]!="Name":
                    if " ".join(parts[:-1])=="Olmec OP900":
                        self.printer_name = " ".join(parts[:-1])
                        self.printer_port = parts[-1]
                        print("Printer found: " +self.printer_name + " Port: "+self.printer_port)

    def printPhoto(self,name):
        print("Started Processing Print: "+name)
        cmd="rundll32.exe C:\WINDOWS\system32\shimgvw.dll ImageView_PrintTo /pt "+self.dir_path+name +" \""+self.printer_name+"\""
        os.system(cmd)
        time.sleep(0.2)
        self.processingPrint()

    def getPrinterStatus(self):
        printer = os.popen("wmic printer list brief").read()
        for line in printer.rsplit('\n'):
            if len(line) >= 5:
                parts = line.rsplit()
                if parts[0] != "Name":
                    if " ".join(parts[:-3]) == "Olmec OP900":
                        return int(parts[-2])

    def processingPrint(self):
        print("Print Sent, Waiting...")
        while self.getPrinterStatus()!=3:
            time.sleep(0.2)
        print("Done!")

if __name__ == '__main__':
    p=Printer()
    p.printPhoto("DSC_1002.JPG")