from PIL import Image

name = "../Resource/Photo/DSC_0009.JPG"
img_file = Image.open(name)
width, height = img_file.size

cover_file = Image.open("../Resource/Image/frame.png")
width2, height2 = cover_file.size

img_file.paste(cover_file, (0, 0), cover_file)
img_file.save("../Resource/Photo/show.jpg")