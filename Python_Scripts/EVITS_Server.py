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
import multiprocessing
import functools
import signal
import keyboard

import numpy as np
import pyvisa

from Impedance_Analyzer_Lib import e4990a_Impedance_Analyzer

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
                time.sleep(1/1000)
                continue
            elif message == b'STRT':
                print('Starting!')
                
            elif message == b'MEAS':
                t1 = time.perf_counter()
                parent_conn.send('MEAS')
                msg = parent_conn.recv()
                if msg == 'DONE':
                    print(msg)
                    t2 = time.perf_counter()
                    print(f' -- {t2-t1} s -- Send/Recv')
                
                self._send_pickle('DONE')
                
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
        print("---- Starting EVITS on {} port {}".format(*host_port_tuple))
        print("---- Waiting for connection...")



def server_process():
    try:
        server = TCPServer(get_server_address(), RequestHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()

def analysis_process():
    pass

def sweeping_process(child_conn, I):
    
    ip_address = I.ip
    number_of_points = I.number_of_points
    number_of_segments = I.number_of_segments
    
    
    # Open PYVISA to Impedance Analyzer
    rm = pyvisa.ResourceManager()

    
    resource_name = f'TCPIP::{ip_address}::INSTR'
    inst = rm.open_resource(resource_name)

    # Timeout must be longer than sweep interval.
    inst.timeout = 30000000

    idn = inst.query('*IDN?').strip()
    opt = inst.query('*OPT?').strip()
    inst.write('*CLS')
    

    # Stop display from updating to speed up measure
    #:DISPlay:ENABle {ON|OFF|1|0}
    inst.write(':DISP:ENAB OFF')
    
    # setup Query
    query = functools.partial(inst.query_ascii_values, separator=',',
                              container=np.array)
    
    number_of_intervals = 1
    bias_current_measurement = np.zeros((1, number_of_intervals),
                                           dtype=np.float32)
    bias_voltage_measurement = np.zeros((1, number_of_intervals),
                                           dtype=np.float32)
    
    # Show marker at peak of trace
    inst.write(':CALC1:MARK1 ON')
    inst.write(':CALC1:MARK1:FUNC:TYPE PEAK')

    
    
    while True:
        try:
            msg = child_conn.recv()
            
            print(msg)
            if msg == 'STOP':
                print('Stoping!')
                break
            
            elif msg == 'MEAS':
                ST = time.perf_counter()
                # Data Containers
                # ydims = number_of_points, number_of_intervals
                # yx = np.zeros(ydims, dtype=np.float32)
                # yr = np.zeros(ydims, dtype=np.float32)
                
                inst.write(':DISP:ENAB OFF')
                inst.write(':SENS1:DC:MEAS:ENAB ON')
            
                
                inst.write(':SOUR:BIAS:STAT ON')
    
                inst.write(':SENS1:DC:MEAS:CLE')
            
                acq_start_time = time.perf_counter()
                inst.write(':TRIG:SING')
                inst.query('*OPC?')
                acq_end_time = (time.perf_counter() - acq_start_time) * 1e3
            
                MSPP = acq_end_time/number_of_points
            
                print(f"Acquisition time is {acq_end_time:.0f} ms")
                print(f"For: {number_of_points:.0f} points")
                print(f"That is: {MSPP:.2f} ms/point")
            
            
                inst.write(':DISP:WIND1:TRAC1:Y:AUTO')
                inst.write(':DISP:WIND1:TRAC2:Y:AUTO')
            
                # Execute marker search
                inst.write(':CALC1:MARK1:FUNC:EXEC')
                inst.write(':SOUR:BIAS:STAT OFF')
            
            
                y = query(':CALC1:DATA:RDAT?')
                # yr[:,0] = y[::2]
                # yx[:,0] = y[1::2]
    
                # R = yr
                # X = yx
            
                ET = time.perf_counter()
                inst.write(':DISP:ENAB ON')
                print(f"Total Time With Overhead: {(ET-ST):.2f} s")
                
                child_conn.send('DONE')
        except KeyboardInterrupt:
            break
            

    



        

        
if __name__ == '__main__':
    print()
    print('////////////////////////////////')
    print('///   EVITS Server')
    print('////////////////////////////////')
    print()
    
    
    
    try:
        #////////////////////////////////
        #// Setup Impedance Analyzer
        #////////////////////////////////
        I = e4990a_Impedance_Analyzer()
        
        
        
        
        measure_Q = multiprocessing.Queue()
        parent_conn, child_conn = multiprocessing.Pipe()
        
        P_server = multiprocessing.Process(target=server_process)
        P_server.start()
        
        P_sweep = multiprocessing.Process(target=sweeping_process, args=(child_conn,I))
        P_sweep.start()
        
        
        time.sleep(1)
        
        
        while True:
            try:
                pass
            except KeyboardInterrupt:
                P_sweep.join()
                P_server.join()
                break
        
          

    except KeyboardInterrupt:
        I.cleanup()
        sys.exit(0)
    except Exception as e:
        P_sweep.terminate()
        P_sweep.join()
        
        P_server.terminate()
        P_server.join()
        I.cleanup()
        traceback.print_exc()
        sys.exit(1)
    else:
        P_sweep.terminate()
        P_sweep.join()
        
        P_server.terminate()
        P_server.join()
        P_server.join()
        I.cleanup()
        sys.exit(0)
