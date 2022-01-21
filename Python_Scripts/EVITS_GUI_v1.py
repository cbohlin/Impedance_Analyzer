#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  6 12:20:57 2022

@author: charlie bohlin
"""

import time
import numpy as np

import tkinter as tk
import tkinter.ttk as ttk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from EVITS_Client import Client



IP_DEFAULT = "10.1.10.62"
C = Client(IP_DEFAULT)
Looping = False


def e4990a_plot(Filename, F, R, X, Low1, High1, Low2, High2):
    Peak = np.argmax(R);

    # fig, ax1 = plt.subplots()
    fig = plt.Figure(figsize=(8,6.5),dpi=100)
    fig.patch.set_facecolor((0.2,0.2,0.2))
    # plt.grid(color=(0.4,0.4,0.4,0.1))
    
    ax1 = fig.add_subplot(111)

    ax1.plot(F/(1e6),R,color=(1, 1, 0))
    ax1.plot(F[Peak]/(1e6),R[Peak]+R[Peak]/10,'vy',markersize=15)
    ax1.set_title(Filename,fontsize=20,color=(1, 1, 1),fontweight='bold')
    ax1.set_xlabel('Frequency (MHz)',fontsize=24,color=(1, 1, 1))
    ax1.set_ylabel('Resistance ($\Omega$)',fontsize=24,color=(1, 1, 0))
    ax1.set_ylim((Low1,High1))
    ax1.set_xlim((np.min(F)/(1e6),np.max(F)/(1e6)))



    ax2 = ax1.twinx()
    ax2.plot(F/(1e6),X,color=(0, 1, 1))
    ax2.set_ylabel('Reactance ($\Omega$)',fontsize=24,color=(0, 1, 1))


    ax1.set_facecolor((0.2,0.2,0.2))
    ax1.spines['bottom'].set_color('w')
    ax1.tick_params(axis='x', colors='w')
    ax1.tick_params(axis='y', colors='w')
    ax2.tick_params(axis='y', colors='w')
    ax2.set_ylim((Low2,High2))


    ax2.text(.04,0.92,f'F = {F[Peak]/(1e6)} MHz',transform=ax2.transAxes,color='y',fontsize=16,fontweight='bold')
    # ax2.text(.04,0.87,f'Acquisition Time = 346 ms',transform=ax2.transAxes,color='g',fontsize=16,fontweight='bold')

    fig.tight_layout()
    # fig = plt.gcf()
    #fig.set_size_inches(10, 7)
    
    return fig


def disconnect_GUI(client):
    try:
        client.cleanup()
    except:
        pass


if __name__ == '__main__':
    controlPanelState = 'disabled'
    connectPanelState = 'normal'
    connectingVal = 0
    consoleList = ['----------------------------------------',
                   'Welcome to the EVITS',
                   '----------------------------------------','']
    
    def on_closing():
        disconnect_GUI(C)
        root.destroy()
     
    def measure(client):
        t1 = time.perf_counter()
        measureButton.config(state='disabled')
        console_message('----')
        console_message('Starting Measure')
        Sweep_Data = client.measure()
        
        
        
        
        f = e4990a_plot(titleEntry.get(), Sweep_Data['Freq'], Sweep_Data['R'], Sweep_Data['X'], -500, 2500, -40000, 1000)
        global plotCanvas
        global plotToolbar
        plotCanvas.get_tk_widget().pack_forget()
        
        
        plotCanvas = FigureCanvasTkAgg(f,plotPanel)
        plotCanvas.get_tk_widget().pack(padx=10)
        
        plotToolbar.pack_forget()
        plotToolbar = NavigationToolbar2Tk(plotCanvas, plotPanel)
        plotToolbar.update()
        

        
        measureButton.config(state='!disabled')
        T = round(time.perf_counter() - t1,3)
        # console_message(f'{T} s')
        console_message('Measure Complete')
        
        
    
    def loop(client):
        global Looping
        if not Looping:
            Looping = True
            loopButton.config(text = "Stop")
            while Looping:
                if not Looping:
                    break
                t1 = time.perf_counter()
                measureButton.config(state='disabled')
                console_message('----')
                console_message('Starting Measure')
                client.measure()
                
                measureButton.config(state='!disabled')
                T = round(time.perf_counter() - t1,3)
                console_message(f'{T} s')
        elif Looping:
            Looping = False
            loopButton.config(text = "Loop")
    
    def connect_impedance_analyzer(client):
        # I = e4990a_Impedance_Analyzer(ipEntry.get())
        
        try:
            __valid_ip(ipEntry.get())
            client.update_ip(ipEntry.get())  
            client.connect()
            # client.cleanup()
            
            connectPanelState = 'disabled'
            controlPanelState = '!disabled'
            
            connectionIndicator.configure(bg='green')
            
            connectButton.config(state=connectPanelState)
            ipEntry.config(state='readonly')
            
            measureButton.config(state=controlPanelState)
            loopButton.config(state=controlPanelState)
            
            console_message(f'Connected to EVITS on: {ipEntry.get()}')
        except:
            console_message('Error Connecting . . .')
        
    
    def console_message(msg):
        consoleList.append(f'{msg}')
        consoleVar.set(value=consoleList)
        #consolePanel.update_idletasks()
        consoleReadout.yview_moveto(1)
        consolePanel.update()
        # consoleReadout.yview_scroll (1,tk.UNITS)
        
        
        
        
    def __valid_ip(ip):
        try:
            L = len(ip.split("."))
        except:
            raise Exception
        
        if L < 4:
            raise Exception
            
            
        
    
    
    root = tk.Tk()
    root.title('EVITS v1')
    root.geometry('1500x950+100+50')
    
    headerFrame = ttk.LabelFrame(root)
    headerFrame.grid(row=0,column=0,sticky=tk.NW,padx=5)
    
    headerSpacer = ttk.Label(headerFrame,text="",font=('Helvetica', '10'),anchor=tk.W,width=75)
    headerSpacer.grid(row=1,column=0)
    
    headerTitle = ttk.Label(headerFrame,text="EVITS: Control Interface",font=('Helvetica', '20'),anchor=tk.W,width=35)
    headerTitle.grid(row=0,column=0)
    
    
    #==============================================================================
    # Connect Panel
    #==============================================================================
    
    connectPanel = ttk.LabelFrame(root,text='Connection')
    connectPanel.grid(row=1,column=0,sticky=tk.NW,padx=5)
    
    ipDefault = tk.StringVar(value=IP_DEFAULT) 
        
    ipEntry = ttk.Entry(connectPanel,width=30,textvariable=ipDefault,state=connectPanelState)
    ipEntry.grid(row=0,column=0,padx=5,pady=5)
    
    
    
    connectButton = ttk.Button(connectPanel, text="Connect",command=lambda:connect_impedance_analyzer(C),state=connectPanelState)
    connectButton.grid(row=0,column=1)
    
    connectionIndicator = tk.Canvas(connectPanel, bg='#ffbdc6', height=20, width=20)
    connectionIndicator.grid(row=0,column=2,padx=10)
    
    connectSpacer = ttk.Label(connectPanel,text="",font=('Helvetica', '10'),anchor=tk.W,width=75)
    connectSpacer.grid(row=1,column=0,columnspan=3)
    
    #==============================================================================
    # Control Panel
    #==============================================================================
    
    controlPanel = ttk.LabelFrame(root,text='Controls')
    controlPanel.grid(row=0,column=1,rowspan=2,sticky=tk.NW,padx=5)
    
    measureButton = ttk.Button(controlPanel, text="Measure", command=lambda:measure(C),state=controlPanelState)
    measureButton.grid(row=0,column=0,sticky=tk.W,padx=5,pady=5)
    
    measureHelp = ttk.Label(controlPanel, text="Takes a single measurement")
    measureHelp.grid(row=0,column=1,sticky=tk.W,padx=5,pady=5)
    
    loopButton = ttk.Button(controlPanel, text="Loop", command=lambda:loop(C),state=controlPanelState)
    loopButton.grid(row=1,column=0,sticky=tk.W,padx=5,pady=5)
    
    loopHelp = ttk.Label(controlPanel, text="Continuously takes measurements. Press again to stop.")
    loopHelp.grid(row=1,column=1,sticky=tk.W,padx=5,pady=5)
    
    
    # controlSpacer = ttk.Label(controlPanel,text="",font=('Helvetica', '10'),anchor=tk.W,width=55)
    # controlSpacer.grid(row=3,column=0)
    
    
    #==============================================================================
    # Console
    #==============================================================================
    consolePanel = ttk.LabelFrame(root,text='Console')
    consolePanel.grid(row=2,column=0,sticky=tk.NW,padx=5)


    consoleVar = tk.StringVar(value=consoleList)

    consoleReadout = tk.Listbox(consolePanel,height=40,width=60,listvariable=consoleVar)
    consoleReadout.grid(row=0,column=0)
    
    consoleSpacer = ttk.Label(consolePanel,text="",font=('Helvetica', '10'),anchor=tk.W,width=75)
    consoleSpacer.grid(row=1,column=0)
    
    
    #==============================================================================
    # Plot Panel
    #==============================================================================
    plotPanel = ttk.LabelFrame(root,text='Impedance Plot')
    plotPanel.grid(row=2,column=1,rowspan=2,sticky=tk.NW,padx=5)
    
    # plotButton = ttk.Button(plotPanel, text="Plot",state=connectPanelState)
    # plotButton.grid(row=0,column=0,sticky=tk.W,padx=5,pady=5)
    titleEntry = ttk.Entry(plotPanel,width = 50)
    titleEntry.pack(pady = 5)
    
    # plotButton.pack()
    
    # f = plt.Figure(figsize=(3,2),dpi=250)
    # sub_plot_1 = f.add_subplot(111)
    # sub_plot_1.plot([1,2,3,4,5,6],[1,5,2,3,4,5])
    
    
    f = e4990a_plot('', np.array([500000,5000000]), np.array([0,0]), np.array([0,0]), -500, 2500, -40000, 1000)
    
   
    plotCanvas = FigureCanvasTkAgg(f,plotPanel)
    plotCanvas.get_tk_widget().pack(padx=10)
    
    plotToolbar = NavigationToolbar2Tk(plotCanvas, plotPanel)
    plotToolbar.update()
    # plotCanvas.get_tk_widget().grid(row=1,column=0,sticky=tk.W,padx=5,pady=5)
    
    plotSpacer = ttk.Label(plotPanel,text="",font=('Helvetica', '10'),anchor=tk.W,width=108)
    plotSpacer.pack()
    
    
    

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

    
    

    
    
    
