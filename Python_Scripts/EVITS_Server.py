#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  7 16:44:11 2022

@author: charlesbohlin

Code skeleton from Ryan Ollos
"""

import argparse
import pickle
import socket
import socketserver
import struct
import sys
import time
import traceback

import numpy as np

BUFSIZE = 4096
HEADER_FORMAT = '4si'
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)


def get_server_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
    except:
        ip = '127.0.0.1'
    else:
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip, 10000


class RequestHandler(socketserver.BaseRequestHandler):

    def setup(self):
        pass

    def handle(self):
        print("Connection from {} port {}".format(*self.client_address))
        while True:
            message, data = self._recv()
            if message is None:
                time.sleep(1/100)
                continue
            elif message == b'STRT':
                print('Starting!')
                
            elif message == b'DISC':
                break
            else:
                print("Unknown message {}".format(message))

    def finish(self):
        print("Connection terminated. Waiting for next connection...")

    def _send_pickle(self, data):
        message = b'PCKL'
        pickled = pickle.dumps(data)
        self._send(pickled, message)

    def _send_bytes(self, data):
        message = b'BYTE'
        bytes_ = data.tobytes()
        self._send(bytes_, message)

    def _send(self, data, message):
        header = struct.pack(HEADER_FORMAT, message, len(data))
        self.request.sendall(header)
        self.request.sendall(data)

    def _recv(self):
        header = self.request.recv(HEADER_SIZE)
        message, rcvsize = struct.unpack(HEADER_FORMAT, header)
        if not message:
            return None, None
        data = None
        if rcvsize:
            pickled = self.request.recv(rcvsize)
            data = pickle.loads(pickled)
        return message, data
        
    def _recv_large(self, bbuf=None):
        BUFSIZE = 4096
        _recv_buf = bytearray(BUFSIZE)
        
        header = self.request.recv(HEADER_SIZE)
        message, rcvsize = struct.unpack(HEADER_FORMAT, header)
        if message in (b'PCKL', b'BYTE'):
            barray = bytearray(rcvsize)
            idx = [0, 0]
            while idx[0] < rcvsize:
                recv_buf_len = \
                    self.request.recv_into(_recv_buf, BUFSIZE)
                idx[1] += recv_buf_len
                if idx[1] > rcvsize:
                    raise Exception("Unexpected receive data size")
                barray[idx[0]:idx[1]] = _recv_buf[:recv_buf_len]
                idx[0] = idx[1]
        else:
            print("Unknown messsage: {}".format(message))
        if message == b'PCKL':
            return pickle.loads(barray)
        elif message == b'BYTE':
            return np.frombuffer(barray, dtype=np.int16)

class TCPServer(socketserver.TCPServer):

    def __init__(self, host_port_tuple, streamhandler):
        super().__init__(host_port_tuple, streamhandler)
        print("Starting EVITS on {} port {}".format(*host_port_tuple))
        print("Waiting for connection...")


def main():
    server = TCPServer(get_server_address(), RequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
    else:
        sys.exit(0)
