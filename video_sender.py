#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket
import threading
import struct
import cv2
import time
import os
import numpy

class WebCamera(object): 
    camera = None
    socket = None
    def __init__(self, resolution = (640, 480), host = ("", 7999)):      
        self.resolution = resolution    
        self.host = host
        self.setSocket(self.host) 
        self.img_quality = 95
        self.flag=0
        
    
    def __del__(self):
        if self.camera !=None:
            self.camera.release()
        if self.socket !=None:
            self.socket.close()
            
    '''
    def setImageResolution(self, resolution):      
        self.resolution = resolution;  
        
    def setHost(self, host):      
        self.host = host;  
    '''    
    def setSocket(self, host): 
        while True:
            try:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
                self.socket.bind(self.host)
                self.socket.listen(5)
                print "Server running on port:%d" % host[1]
                break
            except:
                print 'Socket init error!'
                time.sleep(1)
            
        
    def recv_config(self,client):   
        try:
            info = struct.unpack("lhh",client.recv(8))
        except:
            print 'socket.error'
            return 0
            
        if len(info) != 3:
            print 'Connecting failed! receive config failed!'
            return 0
            
        if info[0]>911:        
            #print info[0]   
            self.img_quality=int(info[0])-911              
            self.resolution=list(self.resolution)        
            self.resolution[0]=info[1]        
            self.resolution[1]=info[2]        
            self.resolution=tuple(self.resolution)  
            print self.resolution              
            return 1    
        else :        
            print 'Connecting failed! receive config failed!'
            return 0
            
    def _processConnection(self, client,addr):   
        if(self.recv_config(client)==0):
            return
            
        self.camera = cv2.VideoCapture(0)
        if self.camera == None:
            print 'Open camera Failed!'
            return
        
        encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),self.img_quality]
        '''           
        f = open("video_info.txt", 'a+')    
        print "Got connection from %s:%d" % (addr[0], addr[1])
        print "Pixel:%d * %d"%(self.resolution[0],self.resolution[1])
        print "Camera open success" 
        print "Connecting start time:%s"%time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
        f.close()    
        '''
        while(1):
            #time.sleep(0.1)
            (grabbed, img) = self.camera.read()
            '''
            cv2.imshow('test',self.img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            '''
            try:
                len(img)
            except:
                self.camera.release()
                print 'Get image failed! maybe camera is in use!'
                return
                
            '''
            if img == None:
                camera.release()
                print 'Get image failed'
                return
            '''
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img  = cv2.resize(img,self.resolution)
            '''
            if self.flag==0:
                self.last_image=img.copy()
                self.flag=1
            dimage=cv2.subtract(img, self.last_image)
            '''
            #img = cv2.GaussianBlur(img,(3,3),0)
            #img = cv2.Canny(img, 50, 150)
            
            #result, img_encoded = cv2.imencode('.jpg',img, encode_param)   
            result, img_encoded = cv2.imencode('.jpg',img)
            img_code = numpy.array(img_encoded)
            img_to_send  = img_code.tostring()

                        
                
            try:
                client.send(struct.pack("lhh",len(img_to_send),
                        self.resolution[0],self.resolution[1])+img_to_send) #发送图片信息(图片长度,分辨率,图片内容)                
            except:
                
                #f = open("video_info.txt", 'a+')            
                print "%s:%d disconnected!" % (addr[0], addr[1])  
                print "Connecting end time:%s"%time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
                print "****************************************"
                self.camera.release()
                #cv2.destroyAllWindows()             
                #f.close()        
                return
            #self.last_image=img.copy()
            
    def run(self):  
        while True:        
            client,addr = self.socket.accept()
            print client,addr
            client.settimeout(2)
            self._processConnection(client, addr)
            '''
            clientThread = threading.Thread(target = self._processConnection, args = (client, addr, ))  #有客户端连接时产生新的线程进行处理                      
            clientThread.start()
            '''
def main():      
    cam = WebCamera()       
    cam.run()
    
if __name__ == "__main__":      
    main()
