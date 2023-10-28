from PIL import Image
 
# Opens a image in RGB mode
number = 2256
im = Image.open(r"F:\Pokemon\Processing\IMG_"+str(number)+".jpg")
 
# Size of the image in pixels (size of original image)
# (This is not mandatory)
width, height = im.size
 
# Setting the points for cropped image

left = 0
top = 0
right = width / 2
bottom = height / 2
 
# Crop immage into 4 quadrants
im1 = im.crop((left, top, right, bottom))
im2 = im.crop((left, bottom, right, height))
im3 = im.crop((right, top, width, bottom))
im4 = im.crop((right, bottom, width, height))

im1 = im1.save(r"F:\Pokemon\Processing\IMG_"+str(number)+"-1.jpg")
im2 = im2.save(r"F:\Pokemon\Processing\IMG_"+str(number)+"-2.jpg")
im3 = im3.save(r"F:\Pokemon\Processing\IMG_"+str(number)+"-3.jpg")
im4 = im4.save(r"F:\Pokemon\Processing\IMG_"+str(number)+"-4.jpg")
# Shows the image in image viewer
#im1.show()

