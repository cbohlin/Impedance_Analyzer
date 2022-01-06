#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  6 12:36:09 2022

@author: otonexus
"""

import numpy as np
import pyvisa


class e4990a_Impedance_Analyzer:
    
    def __init__(self, ip):
        
        # Open PYVISA to Impedance Analyzer
        rm = pyvisa.ResourceManager()

        resource_name = f'TCPIP::{ip}::INSTR'

        inst = rm.open_resource(resource_name)

        idn = inst.query('*IDN?').strip()
        opt = inst.query('*OPT?').strip()

        inst.write('*CLS')
        
        self.IP_addr = ip
        self.inst = inst