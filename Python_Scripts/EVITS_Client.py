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
        self._socket = socket.create_connection(self._server_address,timeout=(3))
        print('Connected to {} port {}'.format(*self._server_address))
        
    def measure(self):
        self._send('MEAS', None)
        self._recv()
        
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
            
    def _recv(self, bbuf=None):
        header = self._socket.recv(self.HEADER_SIZE)
        message, rcvsize = struct.unpack(self.HEADER_FORMAT, header)
        if message in (b'PCKL', b'BYTE'):
            barray = bytearray(rcvsize)
            idx = [0, 0]
            while idx[0] < rcvsize:
                recv_buf_len = \
                    self._socket.recv_into(self._recv_buf, self.BUFSIZE)
                idx[1] += recv_buf_len
                if idx[1] > rcvsize:
                    raise Exception("Unexpected receive data size")
                barray[idx[0]:idx[1]] = self._recv_buf[:recv_buf_len]
                idx[0] = idx[1]
        else:
            print("Unknown messsage: {}".format(message))
        if message == b'PCKL':
            return pickle.loads(barray)
        elif message == b'BYTE':
            return np.frombuffer(barray, dtype=np.int16)      
# if __name__ == '__main__':
#     main()