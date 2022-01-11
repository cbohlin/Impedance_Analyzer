#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  7 16:51:43 2022

@author: charlesbohlin
"""
import configparser
import collections

# Load Config
config = configparser.ConfigParser()
config.read('Evits_Config.ini')


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
    print('True')
else:
    print('False')


# Recast as necessary
config_dict['ip_address'] = config_dict['ip_address']
config_dict['oscillator_voltage'] = float(config_dict['oscillator_voltage'])
config_dict['bias_voltage'] = float(config_dict['bias_voltage'])
config_dict['segments'] = [int(float(k)) for k in config_dict['segments'].split(',')]
config_dict['measurement_speed'] = int(config_dict['measurement_speed'])

print(config_dict)


