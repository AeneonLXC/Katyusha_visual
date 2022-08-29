# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 15:04:16 2022

@MysteriousKnight: 23608
@Email: xingchenziyi@163.com              
 
# ----------------------------------------------
#
#           Katyusha_Vision_main
#               Coding By lxc 
#                  主函数 
#
#          LAST_UPDATE: Wed Mar 23 15:04:16 2022

#
# ----------------------------------------------
 
"""
import cv2 as cv
import numpy as np
import time
from ImagePretreatment.Imager import Imager

# cap = cv.VideoCapture("C:/Users/23608/Desktop/RM_PowerOffice/Video/redlow.mp4")  # 使用第0个摄像头
# cap = cv.VideoCapture("C:/Users/23608/Desktop/RM_PowerOffice/Video/redarmor1.mp4")  # 使用第0个摄像头
cap = cv.VideoCapture("C:/Users/23608/Desktop/RM_PowerOffice/Video/blue_hide1.mp4")  # 使用第0个摄像头
# cap = cv.VideoCapture("C:/Users/23608/Desktop/RM_PowerOffice/Video/步兵.mp4")  # 使用第0个摄像头
# cap = cv.VideoCapture("C:/Users/23608/Desktop/RM_PowerOffice/Video/dxsred.mp4")  # 使用第0个摄像头
# cap = cv.VideoCapture(0)
# blue = cv.imread("D:/testimg/red1.png")
# blue = cv.imread("D:/testimg/blue_temp.png")
ret, frame = cap.read()  # 读取一帧的图像
if __name__ == "__main__":
    img = Imager()
    img.create_trackbars()
    # garyvar = img.create_trackbars()
    while True:
        inf_start = time.time()
        
        ret, frame = cap.read()
        # frame = cv.flip(frame, 1)
        # frame = cv.resize(frame, (1280,720))
        # frame = cv.resize(frame, (360,640))
        dst = img.getGaryBinaryImg(frame)
        mask = img.getHsvBinaryImg(frame)
        result = dst-mask
        fnally = img.mroph_smooth(result)
        
        data_list = img.armor_find(dst)
        second_select_list = img.armor_select(data_list)
        
        armors = img.armor_result(second_select_list)
        for i in range(len(armors)):
            
            # cv.rectangle(frame, 
            #               (int(armors[i][0][0]),int(armors[i][0][1])), 
            #               (int(armors[i][3][0]),int(armors[i][3][1])), 
            #               (0,255,0),5)
            
            cv.circle(frame, (int(armors[i][0][0]),int(armors[i][0][1])), 8, (0,255,0),-1)
            # for j in range(1,5):
            #     cv.line(frame, 
            #             (int(armors[i][j][0]),int(armors[i][j][1])), 
            #             (int(armors[i][j % 5][0]),int(armors[i][j % 5][1])),
            #             (0,255,0),5)
        print(armors)
        inf_end = time.time() - inf_start
        cv.imshow('graygThreshold', dst)
        
        # cv.imshow('hsvBinary', mask)
        # cv.imshow('dstmask', result)
        # cv.imshow('fnally', fnally)
        cv.putText(frame, "FPS: %.2f"%(1/(inf_end+0.0001)), (10, 50),
                cv.FONT_HERSHEY_SIMPLEX, 1.0, (125, 0, 155), 2, 8)
        cv.imshow('frame', frame)
        if cv.waitKey(24) & 0xFF == ord('q'):
            break
    cap.release()  # 释放摄像头
    cv.destroyAllWindows()

    
            

    
