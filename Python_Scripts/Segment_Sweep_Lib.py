#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  6 11:57:28 2022

@author: otonexus
"""

import matplotlib.pyplot as pyplot
import numpy as np
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
        
    all_col_labels = ['OSC Mode','OSC Level',
                  'Bias Mode','Bias Level','Meas Time','Point Avg',
                  'Segment Time','Segment Delay']
    cols = []
    
    
    segm_list = Query2List(I.query(':SENS1:SEGM:DATA?'))
    
    print(segm_list[0:9])
    
    #Each parameter in the above array data is detailed below:
    #<buf>: Always specify 7.
    buff = segm_list[0]
    
    #<stim mode>: Stimulus setting mode
    #0: Specifies with start/stop values
    #1: Specifies with center/span values
    stim_mode = segm_list[1]
    
    if stim_mode == 0:
        cols = ['Start','Stop','Points']
    elif stim_mode == 1:
        cols = ['Center','Span','Points']
    
    # <list OSC level on/off>: ON/OFF of the list OSC level fo each segment
    # 0: OFF, 1: ON
    list_OSC = segm_list[2]
    
    if list_OSC == 1:
        cols.append(all_col_labels[0])
        cols.append(all_col_labels[1])
    
    # <list bias on/off>: ON/OFF of the list bias for each segment
    # 0: OFF, 1: ON
    list_Bias = segm_list[3]
    
    if list_Bias == 1:
        cols.append(all_col_labels[2])
        cols.append(all_col_labels[3])
    
    # <list meas time o/off>: ON/OFF of the meas time setting for each segment
    # 0: OFF, 1: ON
    list_meas_time = segm_list[4]
    
    if list_meas_time == 1:
        cols.append(all_col_labels[4])


    # <list average on/off>: ON/OFF of the average for each segment
    # 0: OFF, 1: ON
    list_average = segm_list[5]
    
    if list_average == 1:
        cols.append(all_col_labels[5])
    
    # <segment time on/off>: ON/OFF of the segment time setting for each segment
    # 0: OFF, 1: ON
    seg_time = segm_list[6]
    
    if seg_time == 1:
        cols.append(all_col_labels[6])
    
    # <delay time on/off>: ON/OFF of the delay time setting for each segment
    # 0: OFF, 1: ON
    delay_time = segm_list[7]  
    
    if delay_time == 1:
        cols.append(all_col_labels[7])
    
    # <segm>: Number of segments. Specify an integer ranging 1 to 201.
    num_segs = segm_list[8]
    
   
    
    
    row_len = int(num_segs)
    col_len = int(len(cols))
    
    segm_data = np.zeros([row_len,col_len])
    print(segm_data)
    
    # print(f'Row:{row_len} Col:{col_len}')
    # print(cols)
    # print(segm_list)

    
    
    return segm_list