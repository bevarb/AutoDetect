'''
2020/11/10
wx
为提高图片中颗粒对比度进行尝试
1：频域方法
2：时域截断，并增强
3：绝对值
'''

import os
import cv2 as cv
import PIL.Image as Image
from PIL import ImageFilter
import numpy as np
import matplotlib.pyplot as plt
def get_fft(img):

    fft = np.fft.fft2(img)
    fft_shift = np.fft.fftshift(fft)
    abs_fft = np.abs(fft_shift)
    abs_fft = np.log(1 + abs_fft)

    return img, abs_fft

def lowPassFilter(image, d):


    f = np.fft.fft2(image)
    fshift = np.fft.fftshift(f)

    def make_transform_matrix(d):
        transfor_matrix = np.zeros(image.shape)
        center_point = tuple(map(lambda x: (x - 1) / 2, fshift.shape))
        for i in range(transfor_matrix.shape[0]):
            for j in range(transfor_matrix.shape[1]):
                def cal_distance(pa, pb):
                    from math import sqrt
                    dis = sqrt((pa[0] - pb[0]) ** 2 + (pa[1] - pb[1]) ** 2)
                    return dis

                dis = cal_distance(center_point, (i, j))
                if dis <= d:
                    transfor_matrix[i, j] = 1
                else:
                    transfor_matrix[i, j] = 0
        return transfor_matrix

    d_matrix = make_transform_matrix(d)
    new_img = np.abs(np.fft.ifft2(np.fft.ifftshift(fshift * d_matrix)))
    return new_img
def GaussianLowFilter(image,d):
    f = np.fft.fft2(image)
    fshift = np.fft.fftshift(f)
    def make_transform_matrix(d):
        transfor_matrix = np.zeros(image.shape)
        center_point = tuple(map(lambda x:(x-1)/2,fshift.shape))
        for i in range(transfor_matrix.shape[0]):
            for j in range(transfor_matrix.shape[1]):
                def cal_distance(pa,pb):
                    from math import sqrt
                    dis = sqrt((pa[0]-pb[0])**2+(pa[1]-pb[1])**2)
                    return dis
                dis = cal_distance(center_point,(i,j))
                transfor_matrix[i,j] = np.exp(-(dis**2)/(2*(d**2)))
        return transfor_matrix
    d_matrix = make_transform_matrix(d)
    new_img = np.abs(np.fft.ifft2(np.fft.ifftshift(fshift*d_matrix)))
    return new_img
root1 = "/media/user/4a9d3177-0660-4271-ac44-f0b688353bfe/Data/ZCH/201014/MCF-7(EV+Exo)-Positive-PBS-10ms-1_1/clear-T5"
name1 = "356.tif"
root2 = "/home/user/wangxu_data/code/2-AutoDetect/Train_Data/high_contrast/JPEGImages"
name2 = "31.tif"
img1 = np.array(Image.open(root1 + "/" + name1))
img2 = np.array(Image.open(root2 + "/" + name2))
img1, fft1 = get_fft(img1)
lp1 = GaussianLowFilter(img1, 150)
ff_d = get_fft(lp1)[1]
img2, fft2 = get_fft(img2)
# img3 = np.reshape(img1, [img1.shape[0], img1.shape[1], 1])
# print(img3.shape)
# img3 = cv.cvtColor(img3, cv.COLOR_GRAY2RGB)
img3_blur = cv.blur(img1, (3, 3))
img3_blur_lp = cv.blur(lp1, (3, 3))
# cv.imwrite("raw.tif", img1)
# cv.imwrite("test.tif", img3_blur_lp.astype(np.uint16))
plt.figure(1)
plt.subplot(221), plt.imshow(img1, "gray"), plt.title("Raw-Low Contrast")
plt.subplot(222), plt.imshow(fft1, "gray"), plt.title("Raw-Low Contrast-FFT")
plt.subplot(223), plt.imshow(lp1, "gray"), plt.title("Raw-Low Contrast-Low-Pass")
plt.subplot(224), plt.imshow(ff_d, "gray"), plt.title("Raw-Low Contrast-Low-Pass-FFT")
plt.figure(2)
plt.subplot(121), plt.imshow(img2, "gray"), plt.title("Raw-High Contrast")
plt.subplot(122), plt.imshow(fft2, "gray"), plt.title("Raw-High Contrast-FFT")
plt.figure(3)
plt.subplot(221), plt.imshow(img1, "gray"), plt.title("Raw-High Contrast-FFT")
plt.subplot(222), plt.imshow(img3_blur, "gray"), plt.title("Raw-High Contrast-FFT")
plt.subplot(223), plt.imshow(img3_blur_lp, "gray"), plt.title("Raw-High Contrast-FFT")
plt.show()

