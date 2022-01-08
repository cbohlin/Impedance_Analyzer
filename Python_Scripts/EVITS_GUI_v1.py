#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  6 12:20:57 2022

@author: otonexus
"""

from tkinter import *
from tkinter.ttk import *

from Impedance_Analyzer_Lib import e4990a_Impedance_Analyzer

controlPanelState = 'disabled'
connectPanelState = 'normal'
connectingVal = 0


def connect_impedance_analyzer():
    
    
    I = e4990a_Impedance_Analyzer(ipEntry.get())
    
    connectPanelState = 'disabled'
    controlPanelState = 'normal'
    
    connectionIndicator.configure(bg='green')
    
    connectButton.config(state=connectPanelState)
    ipEntry.config(state='readonly')
    print('Connected')
    

    
    



root = Tk()
root.title('EVITS v1')
root.geometry('1400x800+100+50')

headerFrame = Frame(root)
headerFrame.grid(row=0,column=0)

headerTitle = Label(headerFrame,text="EVITS:",font=(50))
headerTitle.pack()


#==============================================================================
# Connect Panel
#==============================================================================

connectPanel = LabelFrame(root,text='Connection')
connectPanel.grid(row=1,column=0,padx=5)

ipDefault = StringVar(value="10.1.10.102") 

    
ipEntry = Entry(connectPanel,width=30,textvariable=ipDefault,state=connectPanelState)
ipEntry.grid(row=0,column=0,padx=5,pady=5)

connectMessage = '  Connecting to:  '+ipEntry.get()+' . . .   may take 30s to 1 min'


connectButton = Button(connectPanel, text="Connect",command=connect_impedance_analyzer,state=connectPanelState)
connectButton.grid(row=0,column=1)

connectionIndicator = Canvas(connectPanel, bg='#ffbdc6', height=20, width=20)
connectionIndicator.grid(row=0,column=2,padx=10)





root.mainloop()