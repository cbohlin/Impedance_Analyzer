#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 13 16:08:53 2022

@author: otonexus
"""

import argparse
import collections
import configparser
import datetime
import functools
import numbers
import pathlib
import shutil
import subprocess
import sys
import time
import traceback

import matplotlib.pyplot as pyplot
import numpy
import pyvisa
import scipy.io as scio

def pass_sweep():
    pass

def internal_sweep():
    ST = time.perf_counter()
    # Open PYVISA to Impedance Analyzer
    rm = pyvisa.ResourceManager()

    ip_address = '10.1.10.103'

    resource_name = f'TCPIP::{ip_address}::INSTR'


    inst = rm.open_resource(resource_name)

    # Timeout must be longer than sweep interval.
    inst.timeout = 30000000


    idn = inst.query('*IDN?').strip()
    opt = inst.query('*OPT?').strip()


    inst.write('*CLS')
    
    
    inst.write(':SENS1:DC:MEAS:CLE')


    acq_start_time = time.perf_counter()
    inst.write(':TRIG:SING')
    inst.query('*OPC?')
    acq_end_time = (time.perf_counter() - acq_start_time) * 1e3

    MSPP = acq_end_time/number_of_points

    inst.write(':DISP:WIND1:TRAC1:Y:AUTO')
    inst.write(':DISP:WIND1:TRAC2:Y:AUTO')

    # Execute marker search
    inst.write(':CALC1:MARK1:FUNC:EXEC')
    inst.write(':SOUR:BIAS:STAT OFF')


    y = query(':CALC1:DATA:RDAT?')
    ET = time.perf_counter()
    
    print(f"Acquisition time is {acq_end_time:.0f} ms")
    print(f"For: {number_of_points:.0f} points")
    print(f"That is: {MSPP:.2f} ms/point")
    
    print(f"Total Time With Overhead: {(ET-ST):.2f} s")



# Open PYVISA to Impedance Analyzer
rm = pyvisa.ResourceManager()

ip_address = '10.1.10.103'

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

# Linear Display spacing (Freq Base [Lin]  v Order Base[log])
inst.write(':DISP:WIND1:X:SPAC LIN')


fixture = inst.query(':SENS:FIXT:SEL?').strip()


inst.write(':INIT1:CONT ON')
inst.write(':TRIG:SOUR BUS')
inst.write(':CALC1:PAR1:DEF R')
inst.write(':CALC1:PAR2:DEF X')

inst.write(':SENS1:APER:TIME 1')



## Get X/Freq Data
query = functools.partial(inst.query_ascii_values, separator=',',
                          container=numpy.array)

number_of_points = 101#configure_sweep_parameters(inst, cfg)

inst.write(f':SENS1:SWE:POIN {number_of_points}')
inst.write(':SENS1:SWE:TIME 0')
x = query(':SENS1:FREQ:DATA?')    

# Config Voltage
#----------------------------------

# # OSC
# volt = 0.5;
# inst.write(':SOUR1:MODE VOLT')
# inst.write(f':SOUR1:VOLT {volt}')

# #BIAS
# bias_voltage = 37;
# inst.write(':SOUR1:BIAS:MODE VOLT')
# inst.write(f':SOUR1:BIAS:VOLT {bias_voltage}')


inst.write(':SENS1:DC:MEAS:ENAB ON')


inst.write(':SOUR:BIAS:STAT ON')

number_of_intervals = 1
bias_current_measurement = numpy.zeros((1, number_of_intervals),
                                       dtype=numpy.float32)
bias_voltage_measurement = numpy.zeros((1, number_of_intervals),
                                       dtype=numpy.float32)

# Show marker at peak of trace
# inst.write(':CALC1:MARK1 ON')
# inst.write(':CALC1:MARK1:FUNC:TYPE PEAK')

# Data Containers
ydims = number_of_points, number_of_intervals
yx = numpy.zeros(ydims, dtype=numpy.float32)
yr = numpy.zeros(ydims, dtype=numpy.float32)
 


ST = time.perf_counter()
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
ET = time.perf_counter()
yr[:,0] = y[::2]
yx[:,0] = y[1::2]

F = x
R = yr
X = yx


inst.write(':DISP:ENAB ON')




print(f"Total Time With Overhead: {(ET-ST):.2f} s")

print('-- Next --')
time.sleep(3)
internal_sweep()

inst.close()
rm.close()



