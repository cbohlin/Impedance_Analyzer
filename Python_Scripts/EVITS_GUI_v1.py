#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  6 12:20:57 2022

@author: otonexus
"""


from tkinter import *
from tkinter.ttk import *

from EVITS_Client import Client

IP_DEFAULT = "192.168.0.3"
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
     
    def __sweep():
        pass
    
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
            
            sweepButton.config(state=controlPanelState)
            
            console_message(f'Connected to EVITS on: {ipEntry.get()}')
        except:
            console_message('Error Connecting . . .')
        
    
    def console_message(msg):
        consoleList.append(f'{msg}')
        consoleVar.set(value=consoleList)
    def __valid_ip(ip):
        try:
            L = len(ip.split("."))
        except:
            raise Exception
        
        if L < 4:
            raise Exception
            
            
        
    
    
    root = Tk()
    root.title('EVITS v1')
    root.geometry('1400x800+100+50')
    
    headerFrame = LabelFrame(root)
    headerFrame.grid(row=0,column=0,sticky=NW,padx=5)
    
    headerSpacer = Label(headerFrame,text="",font=('Helvetica', '10'),anchor=W,width=75)
    headerSpacer.grid(row=1,column=0)
    
    headerTitle = Label(headerFrame,text="EVITS: Control Interface",font=('Helvetica', '20'),anchor=W,width=35)
    headerTitle.grid(row=0,column=0)
    
    
    #==============================================================================
    # Connect Panel
    #==============================================================================
    
    connectPanel = LabelFrame(root,text='Connection')
    connectPanel.grid(row=1,column=0,sticky=NW,padx=5)
    
    ipDefault = StringVar(value=IP_DEFAULT) 
        
    ipEntry = Entry(connectPanel,width=30,textvariable=ipDefault,state=connectPanelState)
    ipEntry.grid(row=0,column=0,padx=5,pady=5)
    
    connectMessage = '  Connecting to:  '+ipEntry.get()+' . . .   may take 30s to 1 min'
    
    
    connectButton = Button(connectPanel, text="Connect",command= lambda:connect_impedance_analyzer(C),state=connectPanelState)
    connectButton.grid(row=0,column=1)
    
    connectionIndicator = Canvas(connectPanel, bg='#ffbdc6', height=20, width=20)
    connectionIndicator.grid(row=0,column=2,padx=10)
    
    connectSpacer = Label(connectPanel,text="",font=('Helvetica', '10'),anchor=W,width=53)
    connectSpacer.grid(row=1,column=0)
    
    #==============================================================================
    # Control Panel
    #==============================================================================
    
    controlPanel = LabelFrame(root,text='Controls')
    controlPanel.grid(row=2,column=1,sticky=NW,padx=5)
    
    sweepButton = Button(controlPanel, text="Sweep",command=__sweep,state=controlPanelState)
    sweepButton.grid(row=0,column=0)
    
    
    controlSpacer = Label(controlPanel,text="",font=('Helvetica', '10'),anchor=W,width=53)
    controlSpacer.grid(row=3,column=0)
    
    
    #==============================================================================
    # Console
    #==============================================================================
    consolePanel = LabelFrame(root,text='Console')
    consolePanel.grid(row=2,column=0,sticky=NW,padx=5)


    consoleVar = StringVar(value=consoleList)

    consoleReadout = Listbox(consolePanel,height=25,width=46,listvariable=consoleVar)
    consoleReadout.grid(row=0,column=0,padx=2,pady=2)
    
    consoleSpacer = Label(consolePanel,text="",font=('Helvetica', '10'),anchor=W,width=75)
    consoleSpacer.grid(row=1,column=0)
    
    
    def on_closing():
        disconnect_GUI(C)
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

    
    

    
    
    
