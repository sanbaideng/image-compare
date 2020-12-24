from PIL import Image
from PIL import ImageChops

im1 = Image.open("muyu//7.jpg")
im2 = Image.open("muyu//8.jpg")

diff = ImageChops.difference(im2, im1)
print(diff)
