# -*- coding: utf-8 -*-
"""
Created on Thu Jan  6 12:36:09 2022

@author: otonexus
"""

import pyvisa
import configparser

import numpy as np


class E4990AError(Exception):
    """Exception class for all errors raised in this module.
    """

class e4990a_Impedance_Analyzer:
    
    def __init__(self):
        
        config_file = 'Evits_Config.ini'
        
        self.__update_configuration(self.read_config(config_file))
        
        
        
        # Open PYVISA to Impedance Analyzer
        rm = pyvisa.ResourceManager()

        resource_name = f'TCPIP::{self.ip}::INSTR'
        
        try:
            inst = rm.open_resource(resource_name)
        

            idn = inst.query('*IDN?').strip()
            opt = inst.query('*OPT?').strip()

            inst.write('*CLS')
            
            # Timeout must be longer than sweep interval.
            inst.timeout = 30000
            
            
            self.inst = inst  
        except:
            #raise E4990AError('No device found')
            self.__printErr('Could not connect. Check that the IP address is correct and try restarting the impedance analyzer.')
    
    def read_config(self,filename):
        # Load Config
        config = configparser.ConfigParser()
        config.read(filename)


        # Parse Config
        Sections = config.sections()

        Options = []
        config_dict = {}
        for s in Sections:
            Options = config.options(s)
            
            for o in Options:
                config_dict[o] = config[s][o]

        # Error Check
        key_check = ['ip_address', 'oscillator_voltage', 'bias_voltage', 'segments', 'measurement_speed']
        if key_check == list(config_dict.keys()):
            pass
        else:
            raise E4990AError('Config file missing inputs')


        # Recast as necessary
        config_dict['ip_address'] = config_dict['ip_address']
        config_dict['oscillator_voltage'] = float(config_dict['oscillator_voltage'])
        config_dict['bias_voltage'] = float(config_dict['bias_voltage'])
        config_dict['segments'] = [int(float(k)) for k in config_dict['segments'].split(',')]
        config_dict['measurement_speed'] = int(config_dict['measurement_speed'])
        
        return config_dict        
    
    def configure_e4990a(self):
        # Stop display from updating to speed up measure
        #:DISPlay:ENABle {ON|OFF|1|0}
        self.inst.write(':DISP:ENAB OFF')

        # Linear Display spacing (Freq Base [Lin]  v Order Base[log])
        self.inst.write(':DISP:WIND1:X:SPAC LIN')

        # Get the Keysight fixture being used
        self.fixture = self.inst.query(':SENS:FIXT:SEL?').strip()


        self.inst.write(':INIT1:CONT ON')
        
        # Trigger source set to bus (Python PYVISA)
        self.inst.write(':TRIG:SOUR BUS')
        
        # Plot Resistance (R) and reactance (X)
        self.inst.write(':CALC1:PAR1:DEF R')
        self.inst.write(':CALC1:PAR2:DEF X')

        self.inst.write(':SENS1:APER:TIME 1')
        
        
        # Config Voltage
        #----------------------------------
        # OSC
        self.inst.write(':SOUR1:MODE VOLT')
        self.inst.write(f':SOUR1:VOLT {self.osc_voltage}')
        
    
        #BIAS
        self.inst.write(':SOUR1:BIAS:MODE VOLT')
        self.inst.write(f':SOUR1:BIAS:VOLT {self.bias_voltage}')

        # Allow impedance analyzer to measure DC bias
        self.inst.write(':SENS1:DC:MEAS:ENAB ON')
        
        # Frequency Range
        #-----------------------------------
        
     
    def run_sweep(self):
        pass
        
     
    def __printErr(self,msg):
        print()
        print(f'Error: {msg}')
        print()
        
        
    
    def __update_configuration(self,config_dict):
        self.ip = config_dict['ip_address']
        
        self.osc_voltage = config_dict['oscillator_voltage']
        self.bias_voltage = config_dict['bias_voltage']
        self.segments = config_dict['segments']
        self.measure_speed = config_dict['measurement_speed']
        
        
if __name__ == '__main__':
    I  = e4990a_Impedance_Analyzer()
    A = I.segments
        
        