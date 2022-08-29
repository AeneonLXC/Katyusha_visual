# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 16:31:30 2022

@MysteriousKnight: 23608
@Email: xingchenziyi@163.com   
 
# ----------------------------------------------
#
#           Katyusha_Vision_Module_Config
#               Coding By lxc
#                  Config
#
#          LAST_UPDATE: Wed Mar 23 16:31:30 2022
#
# ----------------------------------------------
存放相关配置文件
"""
from Model import Global_Config

class Config():
    def __init__(self,armor="blue",morphology="open"):
        self.armor_tips = armor
        #   灰度二值化操作参数
        self.GRAY_THRESHOLD = Global_Config.gary_img_threshold["gary"]
        self.GRAY_MAXVAR = Global_Config.gary_img_threshold["maxvar"]
        
        #   形态学操作参数 膨胀腐蚀
        if morphology=="open":
            self.morphology_name = "open"
            self.morph = Global_Config.morphology_create["open"]
        if morphology=="close": 
            self.morphology_name = "close"
            self.morph = Global_Config.morphology_create["close"]
        if morphology=="tophat": 
            self.morphology_name = "tophat"
            self.morph = Global_Config.morphology_create["tophat"]
        if morphology=="blackhat": 
            self.morphology_name = "blackhat"
            self.morph = Global_Config.morphology_create["blackhat"]
            
        #   滤波
        self.gauss = Global_Config.smooth_create["gauss"]
        self.boxfilter = Global_Config.smooth_create["boxfilter"]
        self.blur = Global_Config.smooth_create["blur"]
            
        self.max_morphology = Global_Config.morphology_create["max_morphology"]
        
        #   装甲板筛选操作参数
        #light area
        self.ARMOE_THRESHOLD_MIN=Global_Config.area_threshold["areamin"]
        self.ARMOE_THRESHOLD_MAX=Global_Config.area_threshold["areamax"]
        #>小装甲板
        self.SMALL_ARMOR_WIDTH=Global_Config.small_armor_detect_config["width"]
        self.SMALL_ARMOR_HEIGHT=Global_Config.small_armor_detect_config["height"]
        self.SMALL_ARMOR_RATIO=Global_Config.small_armor_detect_config["w_h_ratio"]
        #>大装甲板
        
        #   HSV 红蓝色域选择配置
        if armor == "red":
            self.hmin = Global_Config.enemy_blue_threshold['hmin']
            self.hmax = Global_Config.enemy_blue_threshold['hmax']
            self.smin = Global_Config.enemy_blue_threshold['smin']
            self.smax = Global_Config.enemy_blue_threshold['smax']
            self.vmin = Global_Config.enemy_blue_threshold['vmin']
            self.vmax = Global_Config.enemy_blue_threshold['vmax']
        #   armor == "blue"
        else:
            self.hmin1 = Global_Config.enemy_red_threshold['hmin1']
            self.hmin2 = Global_Config.enemy_red_threshold['hmin2']
            self.hmax1 = Global_Config.enemy_red_threshold['hmax2']
            self.hmax2 = Global_Config.enemy_red_threshold['hmax2']
            self.smin = Global_Config.enemy_red_threshold['smin']
            self.smax = Global_Config.enemy_red_threshold['smax']
            self.vmin = Global_Config.enemy_red_threshold['vmin']
            self.vmax = Global_Config.enemy_red_threshold['vmax']



            