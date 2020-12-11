from PIL import Image
import imagehash


def compareIH(imgPath1, imgPath2, cutoff=4):
  hash0 = imagehash.average_hash(Image.open(imgPath1))
  hash1 = imagehash.average_hash(Image.open(imgPath2))

  if hash0 - hash1 < cutoff:
    #print('images are similar')
    return True
  else:
    #print('images are not similar')
    return False

if __name__ == '__main__':
	compareIH("top\\147.jpg","top\\146.jpg")