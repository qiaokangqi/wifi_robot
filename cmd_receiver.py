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
    
    def __init__(self, host_addr = ('', 7997)):
        self.host_addr = host_addr
        self.cmd_reception_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.cmd_reception_socket.bind(self.host_addr)

    def parse_receive_op_code(self, op_code):
        if len(op_code) != 2:
                return False
            
        if op_code[0] == '0':
            print 'Motion operation！'
            
            if op_code[1] == '0':
                print 'Front'
            elif op_code[1] == '1':
                print 'Back'
            elif op_code[1] == '2':
                print 'Left'
            elif op_code[1] == '3':
                print 'Right'
            elif op_code[1] == '4':
                print 'Left-front'   
            elif op_code[1] == '5':
                print 'Left-back'
            elif op_code[1] == '6':
                print 'Right-front'
            elif op_code[1] == '7':
                print 'Right-back' 
                
        elif op_code[0] == '1':
            print 'Arm opration'
            
            if op_code[1] == '0':
                print 'Front'
            elif op_code[1] == '1':
                print 'Back'
            elif op_code[1] == '2':
                print 'Left'
            elif op_code[1] == '3':
                print 'Right'
            elif op_code[1] == '4':
                print 'Left-front'   
            elif op_code[1] == '5':
                print 'Left-back'
            elif op_code[1] == '6':
                print 'Right-front'
            elif op_code[1] == '7':
                print 'Right-back' 
            elif op_code[1] == '8':
                print 'Up'
            elif op_code[1] == '9':
                print 'Down' 
            elif op_code[1] == 'a':
                print 'Auto recycle' 
                
        return True
            

    def run_thread(self):
        while True:  
            data, addr = self.cmd_reception_socket.recvfrom(2048)  
            
            if not data:  
                print "client has exist"  
                break  
            print "received:", data, "from", addr  
            #print type(data)
            
            self.parse_receive_op_code(data)
            
    
    def run(self):
        reception_thread = threading.Thread(target = self.run_thread)                        
        reception_thread.start()
          
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
    while True:
        pass
    
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