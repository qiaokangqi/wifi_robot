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

import wx

import video_receiver_ui_base

import video_receiver

class main_frame(video_receiver_ui_base.video):
    def __init__(self, parent,params = None, fps=15):
        video_receiver_ui_base.video.__init__(self, parent)

        
        '''
        self.capture = cv2.VideoCapture(0)
        ret, frame = self.capture.read()
        height, width = frame.shape[:2]
        
        self.capture.release()
        '''
        
        #frame = cv2.imread('logo.jpg',0) 
        '''
        height, width = frame.shape[:2]
        
        self.SetSize((width, height))
        
        print frame.shape[:2]
        self.bmp = wx.BitmapFromBuffer(width, height, frame)
        '''
        
        self.bmp = None
        

        #self.video_sizer.Add( self.bmp, 0, wx.ALL, 5 )

        '''
        self.timer = wx.Timer(self)
        self.timer.Start(1000./fps)
        '''
        #self.Bind(wx.EVT_PAINT, self.OnPaint)
        '''
        self.Bind(wx.EVT_TIMER, self.NextFrame)
        '''
        rec_thread=threading.Thread(target=self.receive_thread) 
        rec_thread.start()
        
    def receive_thread(self):
        while True:
            print "\nCreating connecting..."  
            self.cam = video_receiver.webCamConnect(window = self)  
            #cam.check_config()    
            print "Pixel:%d * %d"%(self.cam.resolution[0],self.cam.resolution[1])
            print "Destination ip: %s:%d"%(self.cam.remoteAddress[0],self.cam.remoteAddress[1])
            if self.cam.connect() == False:
                time.sleep(1)
                continue
            self.cam.getData(self.cam.interval);  

    def OnPaint(self, evt):
        dc = wx.BufferedPaintDC(self)
        dc.DrawBitmap(self.bmp, 0, 0)

    '''
    def NextFrame(self, event):
        ret, frame = self.capture.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.bmp.CopyFromBuffer(frame)
            self.Refresh()
    '''

if __name__ == '__main__':
    app = wx.App(False)
    frame = main_frame(None)
    frame.Show(True)
    app.MainLoop()
    sys.exit('end')

'''
class ShowCapture(wx.Panel):
    def __init__(self, parent, capture, fps=15):
        wx.Panel.__init__(self, parent)

        parent.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        video_sizer = wx.BoxSizer( wx.VERTICAL )

        self.capture = capture
        ret, frame = self.capture.read()

        height, width = frame.shape[:2]
        parent.SetSize((width, height))
        #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        self.bmp = wx.BitmapFromBuffer(width, height, frame)
        
        video_sizer.Add( self.bmp, 0, wx.ALL, 5 )

        self.timer = wx.Timer(self)
        self.timer.Start(1000./fps)

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_TIMER, self.NextFrame)


        parent.SetSizer( video_sizer )
        parent.Layout()
        parent.Centre( wx.BOTH )

    def OnPaint(self, evt):
        dc = wx.BufferedPaintDC(self)
        dc.DrawBitmap(self.bmp, 0, 0)

    def NextFrame(self, event):
        ret, frame = self.capture.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.bmp.CopyFromBuffer(frame)
            self.Refresh()


capture = cv2.VideoCapture(0)
#capture.set(cv.CV_CAP_PROP_FRAME_WIDTH, 320)
#capture.set(cv.CV_CAP_PROP_FRAME_HEIGHT, 240)

app = wx.App()
frame = wx.Frame(None)
cap = ShowCapture(frame, capture)
frame.Show()
app.MainLoop()
'''