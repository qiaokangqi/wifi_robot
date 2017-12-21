#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket
import threading
import struct
import os
import time
import types

class CmdReceiver(object):
    cmd_reception_socket = None
    host_addr = None
    
    def __init__(self, host_addr = ('192.168.5.175', 7997)):
        self.host_addr = host_addr
        self.cmd_reception_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.cmd_reception_socket.bind(self.host_addr)

    def run_thread(self):
        while True:  
            data, addr = self.cmd_reception_socket.recvfrom(2048)  
            
            if not data:  
                print "client has exist"  
                break  
            print "received:", data, "from", addr  
            #print type(data)
            
            if len(data) != 2:
                continue
            
            if data[0] == '0':
                print 'Motion operation！'
                
                if data[1] == '0':
                    print 'Front'
                elif data[1] == '1':
                    print 'Back'
                elif data[1] == '2':
                    print 'Left'
                elif data[1] == '3':
                    print 'Right'
                elif data[1] == '4':
                    print 'Left-front'   
                elif data[1] == '5':
                    print 'Left-back'
                elif data[1] == '6':
                    print 'Right-front'
                elif data[1] == '7':
                    print 'Right-back' 
                    
            elif data[0] == '1':
                print 'Arm opration'
                
                if data[1] == '0':
                    print 'Front'
                elif data[1] == '1':
                    print 'Back'
                elif data[1] == '2':
                    print 'Left'
                elif data[1] == '3':
                    print 'Right'
                elif data[1] == '4':
                    print 'Left-front'   
                elif data[1] == '5':
                    print 'Left-back'
                elif data[1] == '6':
                    print 'Right-front'
                elif data[1] == '7':
                    print 'Right-back' 
                elif data[1] == '8':
                    print 'Up'
                elif data[1] == '9':
                    print 'Down' 
                elif data[1] == 'a':
                    print 'Auto recycle' 
            
    
    def run(self):
        reception_thread = threading.Thread(target = self.run_thread)                        
        reception_thread.start()
        while True:
            pass
          
    '''
    def connect_robot(self):
        pass
    '''
    
    def __del__(self):
        if self.cmd_reception_socket != None:
            self.cmd_reception_socket.close()
    
if __name__ == "__main__":  
    cmd_receiver = CmdReceiver()
    cmd_receiver.run()
    
'''    

address = ('192.168.5.175', 7998)  
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
s.bind(address)  
  
while True:  
    data, addr = s.recvfrom(2048)  
    if not data:  
        print "client has exist"  
        break  
    print "received:", data, "from", addr  
  
s.close()  
'''