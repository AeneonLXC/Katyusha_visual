import cv2 as cv
import numpy as np
import os
path = os.getcwd()

blue_img = os.listdir(path + "\\blue\\num_4\\")
for i in range(len(blue_img)):
    frame = cv.imread(path + "\\blue\\num_4\\" + str(blue_img[i]))
    img = cv.resize(frame, (224,112))
    cv.imwrite(path + "\\blue\\num_4\\" + str(blue_img[i]), img) # 保存ROI区域
