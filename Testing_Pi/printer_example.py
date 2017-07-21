import sys,os

dir_path = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
dir_path += "\Resource\Photo\\"
name="show.jpg"
print(dir_path)
os.system("wmic printer get name,portname")
p_name='"CutePDF Writer"'
os.system("print /d:COM3 "+dir_path+name)
os.system("wmic printer list brief")
# #os.system("print /d:COM3 "+dir_path+name)