#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket
import threading
import struct
import os
import time

class RemoteControl(object):
    cmd_transmission_socket = None
    destination_addr = None
    
    def __init__(self, destination_addr = ('192.168.5.175', 7997)):
        self.cmd_transmission_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.destination_addr = destination_addr

    def run_thread(self):
        while True:  
            msg = raw_input()  
            '''
            if not msg:  
                break  
            '''
            self.cmd_transmission_socket.sendto(msg, self.destination_addr)
    
    def run(self):
        transmission_thread = threading.Thread(target = self.run_thread)                        
        transmission_thread.start()
        while True:
            pass
          
    '''
    def connect_robot(self):
        pass
    '''
    
    def __del__(self):
        if self.cmd_transmission_socket != None:
            self.cmd_transmission_socket.close()
    
if __name__ == "__main__":  
    remote_control = RemoteControl()
    remote_control.run()
        