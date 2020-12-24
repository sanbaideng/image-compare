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


def getAverageHashOfImage(imgPath):
    return imagehash.average_hash(Image.open(imgPath))


def compareNew(hash0, image, minRatePicDic, cutoff=4):
    #hash0 = imagehash.average_hash(Image.open(imgPath1))
    hash1 = imagehash.average_hash(image)
    res = abs(hash0-hash1)
    if hash0 - hash1 < cutoff or hash1 - hash0 < cutoff:
        #print('images are similar')
        return True
    else:
        if res < minRatePicDic['rate']:
            minRatePicDic['image'] = image
            minRatePicDic['rate'] = res

        return False
        #print('images are not similar')


def compareNew2(hash0, hash1, index0, index1, minRatePicDic, cutoff=4):
    #hash0 = imagehash.average_hash(Image.open(imgPath1))
    #hash1 = imagehash.average_hash(image)
    res = abs(hash0-hash1)
    if hash0 - hash1 < cutoff:
        #print('images are similar')
        return True
    else:
        if res < minRatePicDic['rate'] and index1 > index0:
            minRatePicDic['image'] = index1
            minRatePicDic['rate'] = res
        return False


# if __name__ == '__main__':
#     compareIH("7.jpg", "1.png")
