import os
dir_path = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)),os.pardir))
dir_path+="\Resource\Photo\\"
print(dir_path)
dir='"C:/Program Files (x86)/digiCamControl/CameraControlCmd.exe"'
name="test_image.jpg"
os.system(dir + "/filename "+dir_path+name+" /capture ")