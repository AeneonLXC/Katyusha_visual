# -*- coding: utf-8 -*-
"""
Created on Sat Nov 27 11:40:16 2021

@MysteriousKnight: 23608
@Email: xingchenziyi@163.com   
 
# ----------------------------------------------
#
#           Katyusha_Vision_ModuleName_model
#               Coding By lxc
#                  模块name
#
#          LAST_UPDATE: Sat Nov 27 11:40:16 2021
#
# ----------------------------------------------

"""

import cv2 as cv
import numpy as np
import copy
cap = cv.VideoCapture("C:/Users/23608/Desktop/RM_PowerOffice/Video/redup.mp4")  # 使用第0个摄像头

hmin2 = 0
smin = 43
hmin1 = 165
vmin = 46
hmax1 = 180
hmax2 = 34
smax = 255
vmax = 255

def setAngle(xmin , ymin, xmax, ymax):
    """
    角度解算函数
    
    Parameters
    ----------
    xmin : int
        目标的最小x坐标
    ymin : intW
        目标的最小y坐标
    xmax : int
        目标的最大x坐标
    ymax : int
        目标的最大y坐标.

    Returns setAngle
    -------
    None.

    """
    w = 49.64 / 2 # 单位 mm
    h = 65.06 / 2
    # 图像的四点坐标
    point = np.array([
        [ymax, xmax], 
        [ymin, xmax], 
        [ymin, xmin],   
        [ymax, xmin]
        ],dtype=np.float64)
    # 世界坐标
    objectPoints = np.array([
        [-w, -h, 0],
        [w, -h, 0],
        [w, h, 0],
        [-w, h, 0]
                              ],dtype=np.float64)
    #8mm相机内参矩阵 经过matlab标定得到的 需要用到实验室那个8mm的摄像头 
    
    fx = 968.496673044780
    fy = 968.573358686266
    cx = 344.597232314722
    cy = 224.675066052685
    K = np.array([[fx, 0, cx],
                  [0, fy, cy],
                  [0, 0, 1]], dtype=np.float64)

    cameraMatrix = K

    # 相机畸变系数
        
    distCoeffs = np.array([-0.419966600633986, 0.312866671109218, 0, 0, 0],dtype=np.float64)
    
    retval,rvec,tvec = cv.solvePnP(objectPoints, point, cameraMatrix, distCoeffs)
    
    return retval,rvec,tvec
    

def getAngle(rv,tv):
    """
    获取角度

    Parameters
    ----------
    tv : 旋转矩阵
        solve求解的选择矩阵

    Returns pitchAngle, yawAngle
    -------
    """
    
    # x_pos = tv[0]
    # y_pos = -tv[1]
    # z_pos = tv[2]
    # tan_pitch = (y_pos / np.sqrt(np.square(x_pos) + np.square(z_pos)))
    # tan_yaw = x_pos / z_pos
    # pitch = np.rad2deg(np.arctan2(y_pos, z_pos))
    # yaw = np.rad2deg(np.arctan2(x_pos, z_pos))
    
    # rvec_matrix = cv.Rodrigues(rv)[0]    # 旋转向量->旋转矩阵
    # proj_matrix = np.hstack((rvec_matrix, tv))    # hstack: 水平合并
    # eulerAngles = cv.decomposeProjectionMatrix(proj_matrix)[6]  # 欧拉角
    # pitch, yaw, roll = eulerAngles[0], eulerAngles[1], eulerAngles[2]

    
    # pitchAngle, yawAngle, roll = eulerAngles[0], eulerAngles[1], eulerAngles[2]
    # R = cv.Rodrigues(rv)[0]
    # roll = 180*np.arctan2(-R[2][1], R[2][2])/np.pi
    # pitch = 180*np.arcsin(R[2][0])/np.pi
    # yaw = 180*np.arctan2(-R[1][0], R[0][0])/np.pi
    
    
    return pitch, yaw

def nothing(x):
    pass

def distance(p):
    w = np.sqrt(np.square(p[0][0] - p[1][0]) + np.square(p[0][1] - p[1][1]))
    h = np.sqrt(np.square(p[1][0] - p[2][0]) + np.square(p[1][1] - p[2][1]))
    
    return w,h


ret, frame = cap.read()  # 读取一帧的图像
while True:
    ret, frame = cap.read()  # 读取一帧的图像
    finallyimg = frame
    frame = cv.resize(frame, (960,540))
    # cir
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)  # 转灰
    
    img1 = cv.inRange(hsv, (hmin1,smin,vmin), (hmax1,smax,vmax))
    img2 = cv.inRange(hsv, (hmin2,smin,vmin), (hmax2,smax,vmax))
    redhsv = cv.add(img1, img2)
    
    element = cv.getStructuringElement(cv.MORPH_RECT, (3,3))
    
    redhsv = cv.morphologyEx(redhsv, 2, element)
    
    contours, hierarchy = cv.findContours(redhsv, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    contours = np.array(contours)
    hierarchy = np.array(hierarchy)
    
    
    for i in range(contours.shape[0]):
        if hierarchy[-1][i][2] != -1:
            rect = cv.minAreaRect(contours[hierarchy[-1][i][2]])
            point = cv.boxPoints(rect)
            xmin , ymin, xmax, ymax = np.min(point[:][0]), np.min(point[:][1]), np.max(point[:][0]), np.max(point[:][1])
            
            
            # retval,rvec,tvec = setAngle(xmin , ymin, xmax, ymax)
            # pitch, yaw = getAngle(tvec)
            
            weight, high = distance(point)
            if weight * high <= 600 or weight * high >= 2000 or weight / high <= 0.5 or weight / high >= 1.5:
                continue
            
            # cv.circle(frame, (point[0][0], point[0][1]), 7, (0,0,255),-1)
            # cv.circle(frame, (point[1][0], point[1][1]), 7, (0,0,255),-1)
            # cv.circle(frame, (point[2][0], point[2][1]), 7, (0,0,255),-1)
            # cv.circle(frame, (point[3][0], point[3][1]), 7, (0,0,255),-1)
            cv.circle(frame, (np.max(point[:][0]), np.max(point[:][1])), 20, (0,0,255),-1)
            cv.circle(frame, (np.min(point[:][0]), np.min(point[:][1])), 20, (0,0,255),-1)
            for i in range(4):
                cv.line(frame, (int(point[i][0]), int(point[i][1])), (int(point[(i + 1) % 4][0]), int(point[(i + 1) % 4][1])), (0,255,0),5)
                
    cv.imshow('frame Recognition', frame)
    # cv.imshow('gray Recognition', hsv) 
    # cv.imshow('imgrange Recognition', redhsv)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()  # 释放摄像头
cv.destroyAllWindows()


    

