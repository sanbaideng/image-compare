from PIL import Image
import imagehash


def compare(imgPath1, imgPath2, cutoff=4):
  hash0 = imagehash.average_hash(Image.open(imgPath1))
  hash1 = imagehash.average_hash(Image.open(imgPath2))

  if hash0 - hash1 < cutoff:
    print('images are similar')
  else:
    print('images are not similar')

if __name__ == '__main__':
	compare("top\\147.jpg","top\\146.jpg")