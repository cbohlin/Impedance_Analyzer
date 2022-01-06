#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  6 10:37:18 2022

@author: otonexus
"""

import matplotlib.pyplot as pyplot
import numpy
import pyvisa
import scipy.io as scio

def Query2List(Q):
    delim = Q.strip()
    return_list = [float(n) for n in delim.split(',')]
    
    return return_list

def read_segment_data(I):
    # Segment Table Setup
    # Indicates the array data arranged in the following order 
    # (for the segment sweep table); where N is the number of segments 
    # (specified with <segm>) and n is an integer between 1 and N.
    
    # Data = {<buf>,<stim mode>,<list OSC level on/off>,<list bias on/off>,
    #         <list meas time o/off>,<list average on/off>, <list segment time on/off>,
    #         <list delay time on/off>,<segm>, <star 1>,<stop 1>,<poin>,
    #         [OSC Level type 1],[OSC Level 1],[Bias type 1],[Bias Level 1],
    #         [meas time 1],[averaging factor 1],[segment time 1],[delay time 1], ... 
    #         ,[OSC Level type N],[OSC Level N],[Bias type N],[Bias Level N],
    #         [meas time N],[averaging factor N],[segment time N],[delay time N] }

    # Each parameter in the above array data is detailed below:
    
    
    segm_list = Query2List(I.query(':SENS1:SEGM:DATA?'))
    
    print(segm_list[0:9])
    
    #Each parameter in the above array data is detailed below:
    #<buf>: Always specify 7.
    buff = segm_list[0]
    
    #<stim mode>: Stimulus setting mode
    #0: Specifies with start/stop values
    #1: Specifies with center/span values
    stim_mode = segm_list[1]
    
    # <list OSC level on/off>: ON/OFF of the list OSC level fo each segment
    # 0: OFF, 1: ON
    list_OSC = segm_list[2]
    
    # <list bias on/off>: ON/OFF of the list bias for each segment
    # 0: OFF, 1: ON
    list_Bias = segm_list[3]
    
    # <list meas time o/off>: ON/OFF of the meas time setting for each segment
    # 0: OFF, 1: ON
    list_Bias = segm_list[4]


    # <list average on/off>: ON/OFF of the average for each segment
    # 0: OFF, 1: ON
    list_average = segm_list[5]
    
    # <segment time on/off>: ON/OFF of the segment time setting for each segment
    # 0: OFF, 1: ON
    seg_time = segm_list[6]
    
    # <delay time on/off>: ON/OFF of the delay time setting for each segment
    # 0: OFF, 1: ON
    delay_time = segm_list[7]  
    
    # <segm>: Number of segments. Specify an integer ranging 1 to 201.
    num_segs = segm_list[8]

    
    
    return segm_list

# Open PYVISA to Impedance Analyzer
rm = pyvisa.ResourceManager()

ip_address = '10.1.10.102'

resource_name = f'TCPIP::{ip_address}::INSTR'


inst = rm.open_resource(resource_name)


inst.write('*CLS')

try:
#===============
# Run Commands Here
#--------------------------------------------------------------


    print(inst.query(':SENS1:SEGM:SWE:POIN?'))
    
    # :SENSe<Ch>:SEGMent:DATA?

    Tab = read_segment_data(inst)


#--------------------------------------------------------------
except:
    print('Error')

finally:
    inst.close()
    rm.close()