# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 11:51:36 2023

@TwinkelStar: 李星辰
@Email: xingchenziyi@163.com   
 
# ----------------------------------------------
#
#         Katyusha_Vision_ModuleName_model
#               Coding By lxc
#                  模块name
#
#          LAST_UPDATE: Sun Apr 16 11:51:36 2023
#
# ----------------------------------------------

"""
import cv2 as cv
import numpy as np
import sys
sys.path.append("..")
from CameraParameter import Global_Camera_Config

class armorAngle():
    def __init__(self):
        """
        
        
        Returns
        -------
        None.

        """
        self.K = np.array([[Global_Camera_Config.camera_6mm_k["fx"], 0, Global_Camera_Config.camera_6mm_k["cx"]],
                      [0, Global_Camera_Config.camera_6mm_k["fy"], Global_Camera_Config.camera_6mm_k["cy"]], 
                      [0,  0,  1]])
        self.objectPts = np.array([
                              [0,  Global_Camera_Config.world_point_small_armor["h1"]/2, -Global_Camera_Config.world_point_small_armor["w1"]/2], 
                              [0,  Global_Camera_Config.world_point_small_armor["h1"]/2, Global_Camera_Config.world_point_small_armor["w1"]/2],
                              [0,  -Global_Camera_Config.world_point_small_armor["h1"]/2, Global_Camera_Config.world_point_small_armor["w1"]/2],
                              [0,  -Global_Camera_Config.world_point_small_armor["h1"]/2, -Global_Camera_Config.world_point_small_armor["w1"]/2],
                              ], dtype=np.float32)
        self.distCoeffs = np.array([Global_Camera_Config.camera_6mm_k["k1"], Global_Camera_Config.camera_6mm_k["k2"], 0, 0, 0],dtype=np.float64)

        self.error_frame_size = 6 #时间序列错误帧窗口大小
        self.get_target_size = 4   #卡尔曼重新寻找目标缓冲时间
        self.kalman = cv.KalmanFilter(6, 3) # 4：状态数，包括（x，y，dx，dy）坐标及速度（每次移动的距离）；2：观测量，能看到的是坐标值
        self.kalman.measurementMatrix = np.array([[1, 0, 0, 0, 0, 0],
                                                  [0, 1, 0, 0, 0, 0],
                                                  [0, 0, 1, 0, 0, 0]], np.float32) # 系统测量矩阵
        self.kalman.transitionMatrix = np.array([[1, 0, 0, 1, 0, 0],
                                                 [0, 1, 0, 0, 1, 0],
                                                 [0, 0, 1, 0, 0, 1],
                                                 [0, 0, 0, 1, 0, 0],
                                                 [0, 0, 0, 0, 1, 0],
                                                 [0, 0, 0, 0, 0, 1]],      np.float32) # 状态转移矩阵
        self.kalman.processNoiseCov = np.array([[1, 0, 0, 0, 0, 0],
                                                [0, 1, 0, 0, 0, 0],
                                                [0, 0, 1, 0, 0, 0],
                                                [0, 0, 0, 1, 0, 0],
                                                [0, 0, 0, 0, 1, 0],
                                                [0, 0, 0, 0, 0, 1]], np.float32)*0.03 # 系统过程噪声协方差
        self.current_measurement = np.array((3, 1), np.float32)
        self.last_measurement = np.array((3, 1), np.float32)
        self.current_prediction = np.zeros((3, 1), np.float32)
        self.last_prediction = np.zeros((3, 1), np.float32)
        self.error_frame = 0
        self.lostflag = 1
        self.counter = self.get_target_size

    def solvePnP(self,xmin,ymin,xmax,ymax):
        """
        tips：判断图像是否为空
        return： -1
        """
        imagePts = np.array([[xmin, ymin], 
                             [xmax, ymin], 
                             [xmax, ymax], 
                             [xmin, ymax]], dtype=np.float32)
        ret, rvec, tvec = cv.solvePnP(self.objectPts, imagePts, self.K, self.distCoeffs)
        x = tvec[0][0]
        y = tvec[1][0]
        z = tvec[2][0]
        yaw = np.arctan(x / z) * 180.0 / np.pi;
        pitch = np.arctan(-y / z) * 180.0 / np.pi
        
        return yaw, pitch
    
    def track(self,x,y,z):
        self.last_prediction = self.current_prediction # 把当前预测存储为上一次预测
        self.last_measurement = self.current_measurement # 把当前测量存储为上一次测量

        if self.lostflag == 0:               #有目标的情况下丢目标
            if (abs(self.last_measurement[0] - x) > 15 or abs(self.last_measurement[1] - y) > 15 or abs(self.last_measurement[2] - z) > 15): #步兵移动速度3.5，一帧0.04s
                self.error_frame = self.error_frame + 1
            else:
                self.error_frame = 0

            if self.error_frame > 0 and self.error_frame < self.error_frame_size:
                  self.current_measurement = np.array([[np.float32(self.last_prediction[0])],
                                                 [np.float32(self.last_prediction[1])],
                                                 [np.float32(self.last_prediction[2])]])
            elif self.error_frame >= self.error_frame_size:
                  self.current_measurement = np.array([[np.float32(x)], [np.float32(y)], [np.float32(z)]]) # 当前测量
                  self.lostflag = 1
                  self.error_frame = 0
            elif  self.error_frame == 0:
                  self.current_measurement = np.array([[np.float32(x)], [np.float32(y)], [np.float32(z)]])  # 当前测量
                  self.lostflag = 0
        if self.lostflag == 1:
            self.current_measurement = np.array([[np.float32(x)], [np.float32(y)], [np.float32(z)]])



        self.kalman.correct(self.current_measurement) # 用当前测量来校正卡尔曼滤波器
        self.current_prediction = self.kalman.predict() # 计算卡尔曼预测值，作为当前预测


        #lmx, lmy, lmz = self.last_measurement[0], self.last_measurement[1], self.last_measurement[2] # 上一次测量坐标
        cmx, cmy, cmz = self.current_measurement[0], self.current_measurement[1], self.current_measurement[2] # 当前测量坐标
        #lpx, lpy, lpz = self.last_prediction[0], self.last_prediction[1], self.last_prediction[2] # 上一次预测坐标

        cpx, cpy, cpz = self.current_prediction[0], self.current_prediction[1], self.current_prediction[2] # 当前预测坐标


        if self.lostflag == 1:
            self.counter = self.counter - 1
            if(self.counter == 0):
                self.lostflag = 0
                self.counter = self.get_target_size
            return cmx,cmy,cmz

        else:
            return cpx,cpy,cpz
        
        

                
                