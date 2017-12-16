#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket;  
import threading;  
import struct;  import os;  
import time;  
import sys;
import numpy
import cv2

import re

class webCamConnect:      
    def __init__(self, resolution = [640,480], remoteAddress = ("192.168.0.101", 7999), windowName = "video"):          
        self.remoteAddress = remoteAddress     
        self.resolution = resolution    
        self.name = windowName
        self.mutex = threading.Lock()
        self.src=911+15        
        self.interval=0        
        self.path=os.getcwd()        
        self.img_quality = 5
        self.flag=0
        
    def _setSocket(self):      
        self.socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDTIMEO, 1000)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, 1000)
    def connect(self):      
        self._setSocket()
        self.socket.connect(self.remoteAddress)
        
        
    def _processImage(self):    
        temp = self.socket.send(struct.pack("lhh",self.src,self.resolution[0],self.resolution[1]))
        print temp        
        i=0
        while(1):    
            try:
                info = struct.unpack("lhh",self.socket.recv(8))   
            except:
                continue
            print info
            if len(info) == 0:
                return
            bufSize = info[0]
            if bufSize:           
                 try:                  
                    self.mutex.acquire()          
                    self.buf=b''  #??????????????????????????? 
                    tempBuf=self.buf            
                    
                    while(bufSize):                 #循环读取到一张图片的长度
                        tempBuf = self.socket.recv(bufSize)                

                        bufSize -= len(tempBuf)        
                        self.buf += tempBuf
                        data = numpy.fromstring(self.buf,dtype='uint8')
                        self.image=cv2.imdecode(data,1) 
                        
                        #self.image = cv2.GaussianBlur(self.image,(3,3),0)  
                        
                        self.image = cv2.medianBlur(self.image, 5)
                        #self.image = cv2.bilateralFilter(self.image, 9, 75, 75)
                        #self.image = cv2.morphologyEx(self.image, cv2.MORPH_OPEN, (9,9))
                        
                        cv2.imshow(self.name, self.image)  
                        '''
                        if i%30==0:
                            cv2.imwrite(str(i)+'.jpg', self.image)
                        i=i+1
                        '''
                        
                 except:                
                     print "Receive failed!"            
                     pass;              
                 finally:                
                     self.mutex.release();               
                     if cv2.waitKey(10) == 27:                    
                         self.socket.close()                    
                         cv2.destroyAllWindows()                    
                         print "Abandon connect"           
                         break
                     
            if cv2.waitKey(1) & 0xFF == ord('q'):
                            cv2.destroyAllWindows() 
                            break
    def getData(self, interval):  
        self._processImage()
        '''         
        showThread=threading.Thread(target=self._processImage);     
        showThread.start();    
        '''
        '''
        if interval != 0:   # 非0则启动保存截图到本地的功能  
            saveThread=threading.Thread(target=self._savePicToLocal,args = (interval, 
                ));          
            saveThread.setDaemon(1);          
            saveThread.start();  
        '''
    def setWindowName(self, name):      
        self.name = name; 
    def setRemoteAddress(remoteAddress):      
        self.remoteAddress = remoteAddress;   
    def _savePicToLocal(self, interval):      
        while True:          
            try:              
                self.mutex.acquire();              
                path=os.getcwd() + "\\" + "savePic";              
                if not os.path.exists(path):                  
                    os.mkdir(path);            
                cv2.imwrite(path + "\\" + time.strftime("%Y%m%d-%H%M%S", time.localtime(time.time())) + ".jpg",self.image)        
            except:              
                pass;          
            finally:              
                self.mutex.release();              
                time.sleep(interval);
    def check_config(self):    
        path=os.getcwd()    
        print(path)      
        if os.path.isfile(r'%s\video_config.txt'%path) is False:        
            f = open("video_config.txt", 'w+')        
            print "w = %d,h = %d" %(self.resolution[0],self.resolution[1])
            print "IP is %s:%d" %(self.remoteAddress[0],self.remoteAddress[1])
            print "Save pic flag:%d" %(self.interval)
            print "image's quality is:%d,range(0~95)"%(self.img_quality)  
            f.close()        
            print "Init setting"  
        else:        
            f = open("video_config.txt", 'r+')        
            tmp_data=f.readline(50)#1 resolution
            num_list=re.findall(r"\d+",tmp_data)        
            self.resolution[0]=int(num_list[0])        
            self.resolution[1]=int(num_list[1])        
            tmp_data=f.readline(50)#2 ip,port        
            num_list=re.findall(r"\d+",tmp_data)        
            str_tmp="%d.%d.%d.%d"% (int(num_list[0]),int(num_list[1]),int(num_list[2]),int(num_list[3])) 
            self.remoteAddress=(str_tmp,int(num_list[4]))        
            tmp_data=f.readline(50)#3 savedata_flag
            self.interval=int(re.findall(r"\d",tmp_data)[0])        
            tmp_data=f.readline(50)#3 savedata_flag        
            #print(tmp_data)        
            self.img_quality=int(re.findall(r"\d+",tmp_data)[0]) 
           #print(self.img_quality)        
            self.src=911+self.img_quality        
            f.close()        
            print "Reading setting...."
def main():    
    print "Creating connecting..."  
    cam = webCamConnect();    
    #cam.check_config()    
    print "Pixel:%d * %d"%(cam.resolution[0],cam.resolution[1])
    print "Destination ip: %s:%d"%(cam.remoteAddress[0],cam.remoteAddress[1])
    while True:
        cam.connect();      
        cam.getData(cam.interval);  
    
if __name__ == "__main__":      
    main();  
