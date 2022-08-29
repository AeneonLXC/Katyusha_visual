# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 11:01:15 2021

@MysteriousKnight: lxc
@Email: xingchenziyi@163.com
@function: Global_Config
"""


'''
-----------------
大小装甲板配置 我们莫得英雄。。。
'''

# 装甲板识别配置
# class Enemy:
#     def __init__(self,name):
        
small_armor_detect_config = {
    "width": 1,
    "height": 2,
    "w_h_ratio": 1.1,  # 灯条长宽比例阈值
}

big_armor_detect_config = {
    "w": 1,
    "h": 2,
    "w_h_ratio": 1.1,  # 灯条长宽比例阈值
}

area_threshold = {
    "areamin":100,
    "areamax":700
        }

# lxc:需现场调试
# 敌方为红色时HSV的阈值
enemy_red_threshold = {
    "hmin1": 165,
    "hmax1": 180,
    "hmin2": 0,
    "hmax2": 34,
    "smin": 43,
    "smax": 255,
    "vmin": 46,
    "vmax": 255,
}

# lxc:需现场调试
# 敌方为蓝色时HSV的阈值
enemy_blue_threshold = {
    "hmin": 100,
    "hmax": 124,
    "smin": 43,
    "smax": 255,
    "vmin": 46,
    "vmax": 255,
}
#灰度二值化阈值调整
gary_img_threshold = {
    "gary":247,
    "maxvar":254
    }
#形态学参数调整
morphology_create = {
    "open":5,
    "close":13,
    "tophat":4,
    "blackhat":9,
    "max_morphology":30
    }
#滤波参数调整
smooth_create = {
    "gauss":3,
    "boxfilter":3,
    "blur":3
    }
