# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 14:57:15 2022

@MysteriousKnight: 23608
@Email: xingchenziyi@163.com   
 
# ----------------------------------------------
#
#           Katyusha_Vision_ModuleName_Imager
#               Coding By lxc
#                  ImagePretreatment
#
#          LAST_UPDATE: Wed Mar 23 14:57:15 2022
#
# ----------------------------------------------

"""
import cv2 as cv
import numpy as np
import sys
sys.path.append("..")
from Config import Config
config = Config()

class Imager():
    """
    图像预处理
    """
    def emergeImg(self, rec):
        """
        tips：判断图像是否为空
        return： -1
        """
        if rec is False:
            print("IMG IS NONE!")
            return -1
        
        else:
            print("IMG IS OPEN, PLASE WAIT TIME")
        
    def getGaryBinaryImg(self,frame):
        """
        灰度二值化
        该函数获取到原始的rgb图像，灰度二值化处理后可自由设置阈值，运用开运算、闭运算、顶帽运算、黑帽操作
        return 灰度二值化图
        """
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY) #  转灰度图
        garyvar = cv.getTrackbarPos("GRAY", "graygThreshold") #获取滑块的实时更新值传入cv.threshold函数，用于debug
        ret, dst = cv.threshold(gray, 
                                 garyvar, 
                                 config.GRAY_MAXVAR, 
                                 cv.THRESH_BINARY) #  调用配置文件设定阈值和最大阈值
        
        return dst
    
    
    def getHsvBinaryImg(self, frame):
        """
        hsv二值化_分蓝色_和_红色色域 
        """
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV) #  转灰度图
        #   判断当前我方装甲板是什么颜色 我方红色装甲板就要用蓝色色域 我方蓝色装甲板就要用红色色域
        if config.armor_tips == "red":
            hmin = cv.getTrackbarPos("hmin", config.hsv_window) #获取滑块的实时更新值传入cv.inRange函数，用于debug
            smin = cv.getTrackbarPos("smin", config.hsv_window)
            vmin = cv.getTrackbarPos("vmin", config.hsv_window)
            hmax = cv.getTrackbarPos("hmax", config.hsv_window)
            smax = cv.getTrackbarPos("smax", config.hsv_window) 
            vmax = cv.getTrackbarPos("vmax", config.hsv_window) 
            
            img = cv.inRange(hsv, (hmin,smin,vmin), (hmax,smax,vmax))
            hsv_inrange = img
            
            return hsv_inrange
        #   config.armor_tips == "blue"
        elif config.armor_tips == "blue":
            hmin1 = cv.getTrackbarPos("hmin1", config.hsv_window) #获取滑块的实时更新值传入cv.inRange函数，用于debug
            hmax1 = cv.getTrackbarPos("hmax1", config.hsv_window) 
            hmin2 = cv.getTrackbarPos("hmin2", config.hsv_window) 
            hmax2 = cv.getTrackbarPos("hmax2", config.hsv_window)
            smin = cv.getTrackbarPos("smin", config.hsv_window)
            vmin = cv.getTrackbarPos("vmin", config.hsv_window) 
            smax = cv.getTrackbarPos("smax", config.hsv_window)
            vmax = cv.getTrackbarPos("vmax", config.hsv_window)
            img1 = cv.inRange(hsv, (hmin1,smin,vmin), (hmax1,smax,vmax))
            img2 = cv.inRange(hsv, (hmin2,smin,vmin), (hmax2,smax,vmax))
            hsv_inrange = cv.add(img1, img2)
            
            return hsv_inrange
        else: 
            print("未知类型")
            
        
     
    def mroph_smooth(self, img):
        """
        形态学操作_和_滤波操作 获取更加稳定的图像 
        """
        #   获取滑块变量值
        kernel_value = cv.getTrackbarPos(str(config.morphology_name), "graygThreshold")
        #   获取模板结构
        kernel = cv.getStructuringElement(0, (kernel_value,kernel_value))
        #   morphologyEx 可选参数 cv.MORPH_OPEN 开运算 cv.MORPH_CLOSE 闭运算 cv.MORPH_TOPHAT顶帽运算 cv.MORPH_BLACKHAT黑帽运算
        mroph = cv.morphologyEx(img, cv.MORPH_OPEN,kernel)
    
        #   滤波 可选函数 高斯滤波cv.GaussianBlur, 方框滤波cv.boxFilter, 线性滤波cv.blur
        smooth = cv.GaussianBlur(mroph, (config.gauss,config.gauss), 10, 20)
        
        return smooth
        
    def create_trackbars(self):
        """
        创建滑块控制函数
        """
        def nothing(x):
            """Nothing
            """
            pass
        #   灰度二值化滑块var值
        cv.namedWindow("graygThreshold", cv.WINDOW_AUTOSIZE)
        cv.createTrackbar("GRAY", 
                           "graygThreshold", 
                           config.GRAY_THRESHOLD, 
                           config.valuemax, 
                           nothing)
        #   形态学操作滑块
        cv.createTrackbar(str(config.armor_tips), 
                           "graygThreshold", 
                           config.morph, 
                           config.valuemax, 
                           nothing)
        
        #   HSV操作滑块
        if config.armor_tips == 'red':
            cv.namedWindow(config.hsv_window, cv.WINDOW_AUTOSIZE)
            #hmin
            cv.createTrackbar(str(config.hmin_name), 
                               config.hsv_window, 
                               config.hmin, 
                               config.valuemax, 
                               nothing)
            #hmax
            cv.createTrackbar(str(config.hmax_name), 
                               config.hsv_window, 
                               config.hmax, 
                               config.valuemax, 
                               nothing)
            #smin
            cv.createTrackbar(str(config.smin_name), 
                               config.hsv_window, 
                               config.smin, 
                               config.valuemax, 
                               nothing)
            #smax
            cv.createTrackbar(str(config.smax_name), 
                               config.hsv_window, 
                               config.smax, 
                               config.valuemax, 
                               nothing)
            #vmin
            cv.createTrackbar(str(config.vmin_name), 
                               config.hsv_window, 
                               config.vmin, 
                               config.valuemax, 
                               nothing)
            #vmax
            cv.createTrackbar(str(config.vmax_name), 
                               config.hsv_window, 
                               config.vmax, 
                               config.valuemax, 
                               nothing)
        else:
            cv.namedWindow(config.hsv_window, cv.WINDOW_AUTOSIZE)
            #hmin1
            cv.createTrackbar(str(config.hmin1_name), 
                               config.hsv_window, 
                               config.hmin1, 
                               config.valuemax, 
                               nothing)
            #hmax1
            cv.createTrackbar(str(config.hmax1_name), 
                               config.hsv_window, 
                               config.hmax1, 
                               config.valuemax, 
                               nothing)
            #hmin2
            cv.createTrackbar(str(config.hmin2_name), 
                               config.hsv_window, 
                               config.hmin2, 
                               config.valuemax, 
                               nothing)
            #hmax2
            cv.createTrackbar(str(config.hmax2_name), 
                               config.hsv_window, 
                               config.hmax2, 
                               config.valuemax, 
                               nothing)
            #smin
            cv.createTrackbar(str(config.smin_name), 
                               config.hsv_window, 
                               config.smin, 
                               config.valuemax, 
                               nothing)
            #smax
            cv.createTrackbar(str(config.smax_name), 
                               config.hsv_window, 
                               config.smax, 
                               config.valuemax, 
                               nothing)
            #vmin
            cv.createTrackbar(str(config.vmin_name), 
                               config.hsv_window, 
                               config.vmin, 
                               config.valuemax, 
                               nothing)
            #vmax
            cv.createTrackbar(str(config.vmax_name), 
                               config.hsv_window, 
                               config.vmax, 
                               config.valuemax, 
                               nothing)
    def Testdfc(self,img):
        # dp=2
        # miniDist = 100
        # param_1 = 100
        # param_2 = 100
        # min_radius = 20
        # max_radius = 100
        # cv.HoughCircles(image, method, dp, minDist)
        circle = cv.HoughCircles(img,cv.HOUGH_GRADIENT,2,20,
                        param1=100,param2=100,minRadius=50,maxRadius=200)
        
        if circle is None:
            pass
        else:
            for i in range(circle.shape[1]):
                center = (circle[:,i,0][0],circle[:,i,1][0])
                radius = int(circle[:,i,2][0])
                cv.circle(img, (center), radius, (125, 0, 155),3,8,0)
        # print(circle)
        return circle
    
    def armor_find(self,image):
        """
        寻找装甲板轮廓
        Parameters
        ----------
        image : mat
            已经二值化之后的图像.

        Returns
        -------
        contours : 数组
            找到的轮廓.
        hierarchy : TYPE
            DESCRIPTION.

        """
        #find contours
        contours, hierarchy = cv.findContours(image, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        contours = np.array(contours)
        
        
        data_list = self.armor_insert(contours)
        # print("=====")
        # print(contours.shape[0])
        # print("--------")
        # print(hierarchy)
        # print("******")
        # print(data_list)
        return data_list
    
    def armor_insert(self, contours):
        data_list = []
        if contours.shape[0] > 0:
            for i in range(contours.shape[0]):
                data_dict = dict()
                area = cv.contourArea(contours[i])
                rect = cv.minAreaRect(contours[i])
                #rect_x, rect_y为最小外接矩形中心点的坐标
                #rect_w, rect_h最小外界矩形的长和宽
                rect_x, rect_y = rect[0]
                rect_w, rect_h = rect[1]
                z = rect[2]
                if(rect_w < rect_h):
                    rect_w, rect_h = rect_h, rect_w
                    z = float(z) + 90   
                points = cv.boxPoints(rect)
                data_dict["area"] = area
                data_dict["rx"], data_dict["ry"] = rect_x, rect_y
                data_dict["rh"], data_dict["rw"] = rect_h, rect_w
                data_dict["z"] = z
                data_dict["points"] = points
                data_list.append(data_dict)
        return data_list
    
    def armor_select(self, data_list):
        #第一次筛选 
        #根据灯条大小、比例、角度
        first_select_list = []
        if len(data_list) > 0:
            for iter in data_list:
                data_rh, data_rw = iter["rh"], iter["rw"]
                data_area, data_angle = iter["area"], iter["z"]
                if float(data_rw) >= config.SMALL_ARMOR_RATIO * float(data_rh) \
                    and data_area >= config.ARMOE_THRESHOLD_MIN \
                    and data_area < config.ARMOE_THRESHOLD_MAX \
                    and abs(data_angle) > 45. and abs(data_angle) < 135. :
                        first_select_list.append(iter)
        #第二次筛选 
        #根据前后灯条的长度 也就是装甲板的长度 比例 角度 做判断       
        n = len(first_select_list)
        second_select_list = []
        for i in range(n):
            for j in range(i+1,n):
                data_rxi = float(first_select_list[i]["rx"])
                data_rxj = float(first_select_list[j]["rx"])
                
                data_ryi = float(first_select_list[i]["ry"])
                data_ryj = float(first_select_list[j]["ry"])
                
                data_rhi = float(first_select_list[i]["rh"])
                data_rhj = float(first_select_list[j]["rh"])
                
                data_rwi = float(first_select_list[i]["rw"])
                data_rwj = float(first_select_list[j]["rw"])
                
                data_zi = float(first_select_list[i]["z"])
                data_zj = float(first_select_list[j]["z"])
                
                #装甲板的长度
                l_w = np.sqrt((np.square(data_rxi - data_rxj) \
                               + np.square(data_ryi - data_ryj)))
                l_h = (data_rwi + data_rwj) / 2
                #正常来说两个灯条应该处以同一水平线
                if abs(data_zi - data_zj) < 45. \
                    and l_w >= 1.8*l_h \
                    and l_w <= 3.1*l_h:
                    second_select_list.append((first_select_list[i],
                                              first_select_list[j]))

        return second_select_list
        
    def init_points(self,points):
        #重置四点坐标
        xmin = np.min(points[:,0])
        xmax = np.max(points[:,0])
        ymin = np.min(points[:,1])
        ymax = np.max(points[:,1])
        
        point_array = np.array([[xmin,ymin], [xmax,ymin], [xmin,ymax], [xmax,ymax]])
        
        return point_array
        
    def armor_result(self, armor_selected):
        armors = []
        
        for rect_i,rect_j in armor_selected:
            rxi, ryi =  rect_i["rx"], rect_i["ry"]
            pointsi = rect_i["points"]
            boxi = self.init_points(pointsi)
            
            rxj, ryj =  rect_j["rx"], rect_j["ry"]
            pointsj = rect_j["points"]
            boxj = self.init_points(pointsj)
            
            center = [(rxi + rxj) / 2, (ryi + ryj) / 2]
            
            armor_left = [[boxi[0][0], boxi[0][1]], [boxi[2][0], boxi[2][1]]]
            armor_right = [[boxj[1][0], boxj[1][1]], [boxj[3][0], boxj[3][1]]]
            
            armor = [armor_left[0],armor_right[0],armor_right[1],armor_left[1],center]
            armors.append(armor)
            
        return armors
    
    #都看到这里了，还不快退队，再不退队就退不了了（狗头）
    def numberSVM(self, roi):
        """
         roi数字识别

        Parameters
        ----------
        roi : img mat
            对ROI区进行数字识别.

        Returns
        -------
        None.

        """
    
    # def derection(self, input_frame):
        
    #     dst = getGaryBinaryImg(input_frame)
    #     mask = img.getHsvBinaryImg(input_frame)
    #     result = dst-mask
    #     fnally = img.mroph_smooth(result)
        
    #     data_list = img.armor_find(dst)
    #     second_select_list = img.armor_select(data_list)
        
    #     armors = self.armor_result(second_select_list)
        
                
                