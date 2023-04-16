# -*- coding: utf-8 -*-
"""
Created on Wed Nov 10 11:18:02 2021

@MysteriousKnight: 23608
@Email: xingchenziyi@163.com   
 
# ----------------------------------------------
#
#           Katyusha_Vision_ModuleName_model
#               Coding By lxc
#                  Serial_Tool
#
#          LAST_UPDATE: Wed Nov 10 11:18:02 2021
#
# ----------------------------------------------

"""

"""
目前serial_Tools只有配置串口，发送数据这些功能，还有设置起始位，校验位，停止位，接收数据等功能未完善

安装方法 pip install serial
导入方法 from serial_test import Serial_Tool
"""
import serial
import numpy as np
import struct
import time
# 串口对象 
class Serial_Tool:

    def __init__(self, port, bps, timex):
        self.port = port
        self.bps = bps
        self.timex = timex

    def setSerial(self):
        """
        配置串口函数
        Returns 返回串口对象 
        -------
        ser : 串口类 Serial_Tool 
            设置好comx端口，波特率，校验位停止位后返回的对象 .

        """
        try:
            ser = serial.Serial(self.port, self.bps, bytesize=8, parity='N', stopbits=1, timeout=self.timex)
            return ser

        except IOError:  
            print("=======The port is not identified or is occupied !!!=======")
            
        except Exception:
            print("=======setSerial Exception!!!=======")
            
    def getSerialName(self,ser):
        try:
            return  ser.port
        except Exception as e:
            print("=======Not Get Serial Name!!!",e)

    def sendSerial(self ,ser, data1, data2, data3):
        """
        

        Parameters
        ----------
        ser : TYPE
            DESCRIPTION.
        data1 : int
            yaw.
        data2 : int
            pitch.
        data3 : int
            发送开火.

        Returns
        -------
        None.

        """
        try:
            value = 660 / 50
            # data1,data2,data3 = 50,-60,0
            yaw = int(value * data1)  # 映射公式
            pitch = int(value * data2) # 映射公式
            maxv = 50
            # bytes_data = struct.pack('<hhh', yaw, pitch, data3) # '<'表示小端字节序，'h'表示短整型（2字节）
            if yaw < 0 and pitch < 0:
                bytes_data = struct.pack('<hhh', -maxv, -maxv, data3)
            if yaw > 0 and pitch < 0:
                bytes_data = struct.pack('<hhh', maxv, -maxv, data3)
            if yaw > 0 and pitch > 0:
                bytes_data = struct.pack('<hhh', maxv, maxv, data3)
            if yaw < 0 and pitch > 0:
                bytes_data = struct.pack('<hhh', -maxv, maxv, data3)
            # if data1 >= -7 and data1 <= 7:
            #     bytes_data = struct.pack('<hhh', 0, -maxv, data3)
            # if data2 >= -7 and data2 <= 7:
                # bytes_data = struct.pack('<hhh', -maxv, 0, data3)
            if (data1 >= -15 and data1 <= 15) and (data2 >= -7 and data2 <= 7):
                bytes_data = struct.pack('<hhh', 0, 0, data3)
            time.sleep(0.012)
            ser.write(bytes_data) # 发送字节数据
            print("Successful Send Message")
            # print("Not Send Message")
        except Exception as e:
            print("Send Serial Exception!!!",e)
                
    
    def openSerial(self ,ser):

        try:
            return ser.open()    
        except Exception as e:
            print("=======Send Serial Exception!!!",e)
    
    def readSerialTotal(self, ser):
        """
        Parameters
        ----------
        ser : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        try:
            
            if ser.in_waiting != None:  #判断缓冲区的剩余字节数是否为空
                # str_total = ser.readlines()
                return ser.readline()
            else:
                print("=======Serial Data is None!!!=======")
                
        except Exception as e:
            print("=======Read SerialTotal Exception!!!", e)
        
    def closeSerial(self, ser):
        """
        关闭串口，防止端口被重复占用 

        Parameters
        ----------
        ser : serialwin32
            serialwin32.

        Returns 
        -------

        """        
        try:
            return ser.close()
        except Exception as e:
            print("=======Flase Close Serial !!!", e)
        
# if __name__ == "__main__":
#     port = "com4" #设置串口端口
#     bps = 115200 #设置波特率
#     timex = 2 #设置
    
#     xx = Serial_Tool(port,bps,timex)
#     ser = xx.setSerial()

