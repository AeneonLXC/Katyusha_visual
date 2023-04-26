import cv2 as cv
import numpy as np
import os
path = os.getcwd()

train_imgs = []
test_imgs = []
for i in range(150):
    blue_img = os.listdir(path + "\\blue\\num_3\\")
    frame = cv.imread(path + "\\blue\\num_3\\" + str(blue_img[i]))
    gray = img_gray = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
    train_imgs.append(np.array(gray, dtype='float32'))
    test_imgs.append(3)
for i in range(150):
    blue_img = os.listdir(path + "\\blue\\num_4\\")
    frame = cv.imread(path + "\\blue\\num_4\\" + str(blue_img[i]))
    gray = img_gray = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
    train_imgs.append(np.array(gray, dtype='float32'))
    test_imgs.append(4)
for i in range(150):
    blue_img = os.listdir(path + "\\blue\\num_5\\")
    frame = cv.imread(path + "\\blue\\num_5\\" + str(blue_img[i]))
    gray = img_gray = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
    train_imgs.append(np.array(gray, dtype='float32'))
    test_imgs.append(5)
for i in range(150):
    blue_img = os.listdir(path + "\\blue\\small_NULL\\")
    frame = cv.imread(path + "\\blue\\small_NULL\\" + str(blue_img[i]))
    gray = img_gray = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
    train_imgs.append(np.array(gray, dtype='float32'))
    test_imgs.append(0)
    
train_data = np.reshape(np.array(train_imgs, dtype='float32'), (600,-1))
train_label = np.reshape(np.array(test_imgs), (1,-1))

# test_data = train_data[500:,:]
# test_label = train_label[500:]

 
# svm 训练
svm = cv.ml.SVM_create()
svm.setKernel(cv.ml.SVM_LINEAR)
svm.setType(cv.ml.SVM_C_SVC)
svm.setC(2.67)
svm.setGamma(5.383)
result = svm.train(train_data, cv.ml.ROW_SAMPLE, train_label)
svm.save('svm_data.dat')

svm = cv.ml.SVM_load('svm_data.dat')
frame = cv.imread(path + "\\blue\\num_4\\" + "446.jpg")
gray = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
img = np.reshape(np.array(gray, dtype='float32'), (1,-1))
_, y_pred = svm.predict(img)
print(y_pred[0][0])
 
# print(metrics.accuracy_score(test_label, y_pred))