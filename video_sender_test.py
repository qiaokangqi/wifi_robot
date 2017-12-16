#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket;  
import threading;
import struct;
import cv2
import time
import os
import numpy
    
def process_image(client, addr):
    img_quality=0
    resolution=[640,480]
    try:
        info = struct.unpack("lhh",client.recv(8))
    except:
        print 'socket.error'
        return
    if len(info) != 3:
        print 'Connecting failed! receive config failed!'
        return
    
    if info[0]>911:        
            #print info[0]   
            img_quality=int(info[0])-911           
            resolution[0]=info[1]        
            resolution[1]=info[2]        
            resolution=tuple(resolution)
            print resolution
    else :   
        print 'Connecting failed! receive config failed!'
        return 
    
    camera = cv2.VideoCapture(0)  
    if camera == None:
        print 'Open camera Failed!'
        return
    
    encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),img_quality]
    
    while True:
        (grabbed, img) = camera.read()  
        '''
        cv2.imshow('test',self.img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        '''
        try:
            len(img)
        except:
            camera.release()
            print 'Get image failed! maybe camera is in use!'
            return
        
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img  = cv2.resize(img,resolution)   
        
        encode_result, img_encoded = cv2.imencode('.jpg',img, encode_param)     
        img_code = numpy.array(img_encoded)        
        imgdata  = img_code.tostring()  
        
        try:                    
            client.send(struct.pack("lhh",len(imgdata),
                    resolution[0],resolution[1])+imgdata); #发送图片信息(图片长度,分辨率,图片内容)                
        except:              
            print "%s:%d disconnected!" % (addr[0], addr[1])         
            print "Connecting end time:%s"%time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
            print "****************************************"
            camera.release()   
            
            return
    

if __name__ == "__main__":  
    host = ("", 7999)
    socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM);                  
    socket_obj.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1);              
    socket_obj.bind(host);      
    socket_obj.listen(5);      
    print "Server running on port:%d" % host[1]
    while True:
        client,addr = socket_obj.accept()
        print client,addr
        client.settimeout(2)
        process_image(client, addr)
    
