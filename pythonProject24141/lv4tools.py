from PIL import Image
import numpy as np


def readPILimg(image):
    img = Image.open(image)
    return img


def red_values(img):

    red = list(img.getdata(0))
    return red


def green_values(img):

    green = list(img.getdata(1))
    return green


def blue_values(img):

    blue = list(img.getdata(2))
    return blue


def merge_image(r, g, b):
    return Image.merge("RGB", (r, g, b))


def color2gray(img):
    img_gray = img.convert('L')
    return img_gray


def PIL2np(img):
     #nrows = img.size[0]
     #ncols = img.size[1]

    imgarray = np.array(img)
    return imgarray

#-------decompres
def np2PIL(image):
    # print("size of arr: ", image.shape)
    img = Image.fromarray(np.uint8(image))
    return img


def arr_to_PIL(arr):
    return Image.fromarray(arr)


def grayscale_difference(np_gray):
    # Sağındaki piksel ile fark (yatay fark)
    diff_x = np.abs(np_gray[:, 1:] - np_gray[:, :-1])

    # Altındaki piksel ile fark (dikey fark)
    diff_y = np.abs(np_gray[1:, :] - np_gray[:-1, :])

    # Aynı boyuta getirmek için sıfırlarla tamamla
    diff_x = np.pad(diff_x, ((0, 0), (0, 1)), mode='constant', constant_values=0)
    diff_y = np.pad(diff_y, ((0, 1), (0, 0)), mode='constant', constant_values=0)

    # İki farkı birleştirerek genel farkı oluştur
    diff_gray = (diff_x + diff_y) // 2
    return diff_gray