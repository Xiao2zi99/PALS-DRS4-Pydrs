# -*- coding: utf-8 -*-
"""
Created on Sun Nov 14 19:05:20 2021

@author: Vicky Chen
"""

import matplotlib.pyplot as plt
from drs4 import DRS4BinaryFile
import numpy as np
from scipy.signal import find_peaks
import sys
import os

def extractdata(f, channel_list):    
    i = 1
    tempdata_list1 = []  
    tempdata_list2 = [] 
    tempdata_list3 = [] 
    tempdata_list4 = [] 
    data_ID = []
    data_time = []
    data = []
    data_ch1 = []   
    data_ch2 = [] 
    data_ch3 = [] 
    data_ch4 = [] 
    
    while i == 1:         
        event = next(f, "stop")
        print(event)
        #print(channel)
        if event == "stop":
            break
        else:
            for i, channel in enumerate(channel_list):
                if channel == 1:
                    tempdata_list1.append(event.adc_data[boardID][channel]) #event.adc_data[boardID][boardChannel] -> Board nr. 3059 mit Input auf Channel 1
                    list_length = len(tempdata_list1)
                    data_ID.append(event.event_id)
                    data_time.append(event.timestamp)
                        
                    
                    data_ch1 = {"data": tempdata_list1, "identity": data_ID, "time": data_time} 
                    
                elif channel == 2:
                    tempdata_list2.append(event.adc_data[boardID][channel]) #event.adc_data[boardID][boardChannel] -> Board nr. 3059 mit Input auf Channel 1
                    list_length = len(tempdata_list2)
                    data_ID.append(event.event_id)
                    data_time.append(event.timestamp)
                        
                    
                    data_ch2 = {"data": tempdata_list2, "identity": data_ID, "time": data_time} 
                    
                elif channel == 3:
                    tempdata_list3.append(event.adc_data[boardID][channel]) #event.adc_data[boardID][boardChannel] -> Board nr. 3059 mit Input auf Channel 1
                    list_length = len(tempdata_list3)
                    data_ID.append(event.event_id)
                    data_time.append(event.timestamp)
                        
                    
                    data_ch3 = {"data": tempdata_list3, "identity": data_ID, "time": data_time}                 
                    
                elif channel == 4:
                    tempdata_list4.append(event.adc_data[boardID][channel]) #event.adc_data[boardID][boardChannel] -> Board nr. 3059 mit Input auf Channel 1
                    list_length = len(tempdata_list4)
                    data_ID.append(event.event_id)
                    data_time.append(event.timestamp)
                        
                    
                    data_ch4 = {"data": tempdata_list4, "identity": data_ID, "time": data_time}                 
                    
                
            
            data = {"ch1": data_ch1, "ch2": data_ch2, "ch3": data_ch3, "ch4": data_ch4} 
        
      
        #plt.plot(event.adc_data[boardID][channel])
        #plt.show()           
                
    return data
            
def maxvalue(tempdata):
    maxima = []
    for i in range(len(tempdata)):
        maxvalue = np.amax(tempdata[i])
        maxima.append(maxvalue)
    return maxima
####################################
def scaleaxis(x): #Probeweise!!!
    channel = x
    maxenergy = []
    for i in range(len(channel)):
        
        energy = (434/7563)* channel[i] - 5501.59
        maxenergy.append(energy)
    return maxenergy
###################################
def gethist(maxima, bins): 
    hist_arr = np.histogram(maxima, bins=bins)
    return hist_arr

def histogram(maxima, bins, title, xtitle):
    plt.title(title)
    plt.xlabel(xtitle)
    plt.ylabel("Counts")
    plt.hist(maxima[::-1],bins=bins)
    
    ax = plt.gca()
    p = ax.patches
    energy = [patch.get_xy() for patch in p]
    counts = [patch.get_height() for patch in p]    
    hist_data = {"energy": energy, "counts": counts}
    
    plt.yscale('log')
    plt.show()


    return hist_data

def savehistogram(maxima, bins, title, xtitle):
    plt.title(title)
    plt.xlabel(xtitle)
    plt.ylabel("Counts")
    plt.hist(maxima[::-1],bins=bins)
    
    ax = plt.gca()
    p = ax.patches
    energy = [patch.get_xy() for patch in p]
    counts = [patch.get_height() for patch in p]    
    hist_data = {"energy": energy, "counts": counts}
    
    plt.yscale('log')
    plt.show()
    
    dir_input = input("Enter the desired directory for your file: ")
    filename = input("enter a filename (without .*)")

    filepath = "{}{}{}".format(dir_input, os.sep, filename)
    filepath = os.sep.join([dir_input, filename])

    return hist_data
    
    return 0

def peakposition(x):
    peaks, _ = find_peaks(x, prominence=10)
    
    plt.plot(peaks, x[peaks], "xr"); plt.plot(x)
    plt.yscale('log')
    plt.show()
    return peaks


######################################################################################################################################################################################
######################################################################################################################################################################################
######################################################################################################################################################################################

# dir_input = input("Enter the directory of your File: ")
# filename = input("Enter the name of the file (with .bin): ")

# filepath = "{}{}{}".format(dir_input, os.sep, filename)
#filepath = os.sep.join([dir_input, filename])
filepath = 'C:/Users/admin/Desktop/pydrs4/tests/2ch100k.bin'
print(filepath)

with DRS4BinaryFile(filepath) as f:
    
    print(f.board_ids)
    print(f.channels)

    boardID_list = f.board_ids
    boardID = boardID_list[0]
    totalBoards = len(boardID_list)
    boardID = boardID_list[0]
    
    boardCH = f.channels[boardID]
    
    
    data = extractdata(f, boardCH) 
    
    
    i = 1
    while i == 1:
        print("You have connected ", totalBoards, "Board(s) with Channel(s)", boardCH )

        ch_opt = []
        channel = input("Choose between 'ch1','ch2','ch3','ch4': ")
        print("You have selected channel: ", channel)
        
        temp_data = data[channel]
        
        x=1
        while x == 1:
            operations = ['histogram', 'save_data', 'select channel', 'finish']
            print("Caution: If next_channel or finish are selected current data can be overwritten and data might be lost!")
            print("Available operations: ", operations)
            command = input("choose an operation: ")
            
            if command == 'select channel':
                print('you chose select channel')   
                break     
            
            elif command == 'histogram':
                print('you chose histogram')
                title = input("choose a title for your plot: ")
                bins = int(input("choose the number of binaries: "))
                save = input("Do you want to save the plot and data of the histogram?  'yes' or 'no': ")
                
                baseline = 34000
                
                data_corr = -np.array(temp_data['data'])+2*baseline
                maxcounts = maxvalue(data_corr)
                
                if save == 'no':
                    hist_data = histogram(maxcounts, bins, title, 'channel')
            
            elif command == 'save_data':
                print('you chose save_data')

                
            elif command == 'finish':
                print('the program will be closed')   
                break
                
            else:
                print("invalid syntax")
                operations = ['histogram', 'save_data', 'save_hist', 'next_channel', 'finish']
                print("Caution: If next_channel or finish are selected current data can be overwritten and data might be lost!")
                print("Available operations: ", operations)
                command = input("choose an operation: ")
                
        if command == 'finish':
            break       
    
    



