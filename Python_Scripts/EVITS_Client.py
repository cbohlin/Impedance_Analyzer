# -*- coding: utf-8 -*-
"""
Created on Mon Jan 10 09:15:52 2022

@author: charlesbohlin

Code skeleton from Ryan Ollos
"""

import argparse
import array
import cv2
import logging
import multiprocessing
import pickle
import socket
import struct
import sys
import tempfile
import time

import numpy as np

# def main():
#     C = Client('192.168.0.3')
#     C.connect()
#     input('EVITS is up and running. Press [enter] to take a measurement.')
#     input('EVITS is up and running. Press [enter] to take a measurement.')
#     C.start()
#     C.cleanup()

class Client:

    BUFSIZE = 4096
    HEADER_FORMAT = '4si'
    HEADER_SIZE = struct.calcsize(HEADER_FORMAT)

    def __init__(self,ip):
        self._socket = None
        #self._config = config
        self._server_address = (ip, 10000)
        self._recv_buf = bytearray(self.BUFSIZE)
        
    def update_ip(self,ip):
        self._server_address = (ip, 10000)

    def connect(self):
        self._socket = socket.create_connection(self._server_address)
        print('Connected to {} port {}'.format(*self._server_address))
        
    def start(self):
        self._send('STRT', None)
        
    def cleanup(self):
        self._send('DISC', None)
        self._socket.shutdown(socket.SHUT_RDWR)
        self._socket.close()

        
    def _send(self, message, data):
        pickled = pickle.dumps(data) if data is not None else None
        rcvsize = len(pickled) if pickled is not None else 0
        header = struct.pack(self.HEADER_FORMAT, message.encode('utf-8'),
                             rcvsize)
        self._socket.sendall(header)
        if pickled is not None:
            self._socket.sendall(pickled)
            
# if __name__ == '__main__':
#     main()