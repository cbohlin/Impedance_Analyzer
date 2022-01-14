#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  6 12:20:57 2022

@author: otonexus
"""

import time

import tkinter as tk
import tkinter.ttk as ttk

from EVITS_Client import Client

IP_DEFAULT = "10.1.10.62"
C = Client(IP_DEFAULT)

def disconnect_GUI(client):
    try:
        client.cleanup()
    except:
        pass


if __name__ == '__main__':

    controlPanelState = 'disabled'
    connectPanelState = 'normal'
    connectingVal = 0
    consoleList = ['------------------------','Welcome to the EVITS','------------------------','']
     
    def __measure(client):
        while True:
            t1 = time.perf_counter()
            measureButton.config(state='disabled')
            console_message('----')
            console_message('Starting Measure')
            client.measure()
            
            measureButton.config(state='!disabled')
            T = round(time.perf_counter() - t1,3)
            console_message(f'{T} s')
            
    
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
            
            console_message(f'Connected to EVITS on: {ipEntry.get()}')
        except:
            console_message('Error Connecting . . .')
        
    
    def console_message(msg):
        consoleList.append(f'{msg}')
        consoleVar.set(value=consoleList)
        #consolePanel.update_idletasks()
        consolePanel.update()
        
        
    def __valid_ip(ip):
        try:
            L = len(ip.split("."))
        except:
            raise Exception
        
        if L < 4:
            raise Exception
            
            
        
    
    
    root = tk.Tk()
    root.title('EVITS v1')
    root.geometry('1400x800+100+50')
    
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
    controlPanel.grid(row=1,column=1,rowspan=2,sticky=tk.NW,padx=5)
    
    measureButton = ttk.Button(controlPanel, text="Measure", command=lambda:__measure(C),state=controlPanelState)
    measureButton.grid(row=0,column=0,sticky=tk.W,padx=5)
    
    
    controlSpacer = ttk.Label(controlPanel,text="",font=('Helvetica', '10'),anchor=tk.W,width=75)
    controlSpacer.grid(row=3,column=0)
    
    
    #==============================================================================
    # Console
    #==============================================================================
    consolePanel = ttk.LabelFrame(root,text='Console')
    consolePanel.grid(row=2,column=0,sticky=tk.NW,padx=5)


    consoleVar = tk.StringVar(value=consoleList)

    consoleReadout = tk.Listbox(consolePanel,height=25,width=50,listvariable=consoleVar)
    consoleReadout.grid(row=0,column=0)
    
    consoleSpacer = ttk.Label(consolePanel,text="",font=('Helvetica', '10'),anchor=tk.W,width=75)
    consoleSpacer.grid(row=1,column=0)
    
    
    def on_closing():
        disconnect_GUI(C)
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

    
    

    
    
    
