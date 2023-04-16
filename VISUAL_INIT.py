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
 我想把你放在我的心中，就像我把你放在我的内存中一样。
 你是我的最高优先级，我永远不会忘记你。
 你是我的最大空间，我永远不会浪费你。
 你是我的最快速度，我永远不会迟到。
 
 我想给你一个拥抱，就像我给你一个函数调用一样。
 你是我的输入参数，我是你的输出结果。
 我们互相传递，互相返回，互相调用。
 我们的函数就是我们的信任，灵活而强大，没有副作用和泄露。
 
 我想和你一起写代码，就像我们一起写故事一样。
 你是我的主角，我是你的配角。
 我们互相协作，互相支持，互相完善。
 我们的代码就是我们的爱情，简洁而优雅，没有冗余和错误。
"""
import cv2 as cv
import numpy as np
import time
from ImagePretreatment.Imager import Imager
from AngleSolve import armorAngle
from Config import Config
config = Config()

from SendSerial.Serial_Tool import Serial_Tool
port = "com4" #设置串口端口
bps = 115200 #设置波特率
timex = 2 #设置
Serial = Serial_Tool(port,bps,timex)
ser = Serial.setSerial()

# cap = cv.VideoCapture("C:/Users/23608/Desktop/RM_PowerOffice/Video/redlow.mp4")  # 使用第0个摄像头
# cap = cv.VideoCapture("E:/2022机甲大师/RM_PowerOffice/Video/redarmor.mp4")  # 使用第0个摄像头
if 0 == 1:
    if config.armor_tips == "blue":
        cap = cv.VideoCapture("E:/2022机甲大师/RM_PowerOffice/Video/redarmor1.mp4")  # 使用第0个摄像头
    if config.armor_tips == "red":
        cap = cv.VideoCapture("E:/2022机甲大师/RM_PowerOffice/Video/blue_hide1.mp4")  # 使用第0个摄像头
# cap = cv.VideoCapture("E:/2022机甲大师/RM_PowerOffice/Video/步兵.mp4")  # 使用第0个摄像头
# cap = cv.VideoCapture("E:/2022机甲大师/RM_PowerOffice/Video/dxsred.mp4")  # 使用第0个摄像头
else:
    cap = cv.VideoCapture(1)
# blue = cv.imread("D:/testimg/red1.png")
# blue = cv.imread("D:/testimg/blue_temp.png")
ret, frame = cap.read()  # 读取一帧的图像
roi_img = np.zeros((frame.shape[0],frame.shape[1],3))
def swap(x,y):
    if x > y:
        t = x
        x = y
        y = t
    return x,y
if __name__ == "__main__":
    img = Imager()
    angle = armorAngle.armorAngle()
    img.create_trackbars()
    sign = 0
    # garyvar = img.create_trackbars()
    while True:
        inf_start = time.time()
        
        ret, frame = cap.read()
        # frame = cv.flip(frame, 170)
        # frame = cv.resize(frame, (1280,720))

        # if config.armor_tips == "blue":
        #     frame = cv.resize(frame, (640,400))
        # if config.armor_tips == "red":
        #     frame = cv.resize(frame, (360,640))
        dst = img.getGaryBinaryImg(frame)
        mask = img.getHsvBinaryImg(frame)
        result1 = mask-dst
        # result2 = dst-mask
        # fnally = img.mroph_smooth(result1)
        
        data_list = img.armor_find(mask)
        second_select_list = img.armor_select(data_list)
        
        armors = img.armor_result(second_select_list)

        for i in range(len(armors)):
            
            # cv.rectangle(frame, 
            #               (int(armors[i][1][0]),int(armors[i][1][1])), 
            #               (int(armors[i][3][0]),int(armors[i][3][1])), 
            #               (0,255,0),3)
            cv.line(frame, 
                    (int(armors[i][1][0]),int(armors[i][1][1])), 
                    (int(armors[i][4][0]),int(armors[i][4][1])),
                    (0,255,0),3)
            cv.line(frame, 
                    (int(armors[i][2][0]),int(armors[i][2][1])), 
                    (int(armors[i][3][0]),int(armors[i][3][1])),
                    (0,255,0),3)
            
            yaw,pitch = angle.solvePnP(armors[i][1][0],int(armors[i][1][1]),int(armors[i][4][0]),int(armors[i][4][1]))
            if int(armors[i][4][0]) != int(armors[i][1][0]) or int(armors[i][4][1]) != int(armors[i][1][1]):
                
                x1,x2 = swap(int(armors[i][4][0]), int(armors[i][1][0]))
                y1,y2 = swap(int(armors[i][4][1]), int(armors[i][1][1]))
                # roi_img[x1:x2,y1:y2,:] = frame[x1:x2,y1:y2,:]
                
                # cv.imshow('roi', roi_img)
            

            
            # cv.circle(frame, (int(armors[i][0][0]),int(armors[i][0][1])), 8, (0,255,0),-1)
            # for j in range(1,5):
                # cv.line(frame, 
                #         (int(armors[i][j][0]),int(armors[i][j][1])), 
                #         (int(armors[i][j % 5][0]),int(armors[i][j % 5][1])),
                #         (0,255,0),10)
                # cv.line(frame, 
            #         (int(armors[i][j][0]),int(armors[i][j][1])), 
            #         (int(armors[i][j%4][0]),int(armors[i][j%4][1])),
            #         (0,255,0),3)
        # print(armors)
            print("yaw------->",yaw)
            print("pitch----->",pitch)
            
            Serial.sendSerial(ser, yaw, pitch, 1)
        # if(len(armors) == 0):    
            # Serial.sendSerial(ser, 0, 0, 0)
        inf_end = time.time() - inf_start
        cv.imshow('graygThreshold', dst)
        cv.imshow('hsvBinary', mask)
        # cv.imshow('roi', roi)
        # cv.imshow('result1', result1)
        # cv.imshow('dstmask2', result2)
        # cv.imshow('fnally', fnally)
        cv.putText(frame, "FPS: %.2f"%(1/(inf_end+0.0001)), (10, 50),
                cv.FONT_HERSHEY_SIMPLEX, 1.0, (125, 0, 155), 2, 8)
        cv.imshow('frame', frame)
        if cv.waitKey(24) & 0xFF == ord('q'):
            break
    cap.release()  # 释放摄像头
    cv.destroyAllWindows()

    
            

    
