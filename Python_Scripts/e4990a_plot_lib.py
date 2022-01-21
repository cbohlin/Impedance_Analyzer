# -*- coding: utf-8 -*-
"""
Created on Tue Jan 18 15:01:26 2022

@author: charlesbohlin
"""

import argparse
import time
import datetime
import os
from pathlib import Path

import pyvisa
import pyvisa_py
import numpy
import functools

import matplotlib.pyplot as plt
import scipy.io as scio

def e4990a_plot(Filename, F, R, X, Low1, High1, Low2, High2):
    Peak = numpy.argmax(R);


    fig, ax1 = plt.subplots()
    fig.patch.set_facecolor((0.2,0.2,0.2))
    plt.grid(color=(0.4,0.4,0.4,0.1))

    ax1.plot(F/(1e6),R,color=(1, 1, 0))
    ax1.plot(F[Peak]/(1e6),R[Peak]+R[Peak]/10,'vy',markersize=15)
    ax1.set_title(Filename,fontsize=28,color=(1, 1, 1),fontweight='bold')
    ax1.set_xlabel('Frequency (MHz)',fontsize=24,color=(1, 1, 1))
    ax1.set_ylabel('Resistance ($\Omega$)',fontsize=24,color=(1, 1, 0))
    ax1.set_ylim((Low1,High1))
    ax1.set_xlim((numpy.min(F)/(1e6),numpy.max(F)/(1e6)))



    ax2 = ax1.twinx()
    ax2.plot(F/(1e6),X,color=(0, 1, 1))
    ax2.set_ylabel('Reactance ($\Omega$)',fontsize=24,color=(0, 1, 1))


    ax1.set_facecolor((0.2,0.2,0.2))
    ax1.spines['bottom'].set_color('w')
    ax1.tick_params(axis='x', colors='w')
    ax1.tick_params(axis='y', colors='w')
    ax2.tick_params(axis='y', colors='w')
    ax2.set_ylim((Low2,High2))


    ax2.text(.04,0.92,f'F = {F[Peak]/(1e6)} MHz',transform=ax2.transAxes,color='y',fontsize=26,fontweight='bold')
    ax2.text(.04,0.87,f'Acquisition Time = 346 ms',transform=ax2.transAxes,color='g',fontsize=26,fontweight='bold')


    fig = plt.gcf()
    fig.set_size_inches(14.5, 10.5)
    
    Save_Path = str(Path(os.getcwd()).parent)+'/'
    fig.savefig(Save_Path + f'{Filename}.png', dpi=100)