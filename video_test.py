# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 00:19:00 2017

@author: kangChi
"""

import cv2  
import numpy
#import matplotlib.pyplot as plot
import time

cap = cv2.VideoCapture(0)

while(1):
    # get a frame
    time.sleep(0.13)
    ret, frame = cap.read()
    # show a frame
    if frame==None:
        print 'failed'
        continue
    cv2.imshow("capture", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.imwrite('testImg.jpg',frame)
        break

cap.release()
cv2.destroyAllWindows() 