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
import json
import csv

def extractdata(f, channel_list):    
    i = 1
    tempdata_list1 = []  
    tempdata_list2 = [] 
    tempdata_list3 = [] 
    tempdata_list4 = [] 
    
    data_ID1 = []
    data_ID2 = []
    data_ID3 = []
    data_ID4 = []
    
    data_time1 = []
    data_time2 = []
    data_time3 = []
    data_time4 = []
    
    data = []
    data_ch1 = []   
    data_ch2 = [] 
    data_ch3 = [] 
    data_ch4 = [] 
    
    while i == 1:         
        event = next(f, "stop")
        #print(event)
        #print(channel)
        if event == "stop":
            break
        else:
            for i, channel in enumerate(channel_list):
                if channel == 1:
                    tempdata_list1.append(event.adc_data[boardID][channel]) #event.adc_data[boardID][boardChannel] -> Board nr. 3059 mit Input auf Channel 1
                    list_length = len(tempdata_list1)
                    data_ID1.append(event.event_id)
                    data_time1.append(event.timestamp)
                        
                    
                    data_ch1 = {"data": tempdata_list1, "identity": data_ID1, "time": data_time1} 
                    
                elif channel == 2:
                    tempdata_list2.append(event.adc_data[boardID][channel]) #event.adc_data[boardID][boardChannel] -> Board nr. 3059 mit Input auf Channel 1
                    list_length = len(tempdata_list2)
                    data_ID2.append(event.event_id)
                    data_time2.append(event.timestamp)
                        
                    
                    data_ch2 = {"data": tempdata_list2, "identity": data_ID2, "time": data_time2} 
                    
                elif channel == 3:
                    tempdata_list3.append(event.adc_data[boardID][channel]) #event.adc_data[boardID][boardChannel] -> Board nr. 3059 mit Input auf Channel 1
                    list_length = len(tempdata_list3)
                    data_ID3.append(event.event_id)
                    data_time3.append(event.timestamp)
                        
                    
                    data_ch3 = {"data": tempdata_list3, "identity": data_ID3, "time": data_time3}                 
                    
                elif channel == 4:
                    tempdata_list4.append(event.adc_data[boardID][channel]) #event.adc_data[boardID][boardChannel] -> Board nr. 3059 mit Input auf Channel 1
                    list_length = len(tempdata_list4)
                    data_ID4.append(event.event_id)
                    data_time4.append(event.timestamp)
                        
                    
                    data_ch4 = {"data": tempdata_list4, "identity": data_ID4, "time": data_time4}                 
                    
                
            
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

def savehistogram(hist_data):    
    ##### saving 
    dir_input = input("Enter the desired directory for your file: ")
    filename = input("enter a filename (without .*)")

    filepath = "{}{}{}".format(dir_input, os.sep, filename)
    filepath = os.sep.join([dir_input, filename])
    
    tupleenergy = hist_data["energy"]
    energy =[]
    
    for i in range(len(tupleenergy)):
        energy.append(tupleenergy[i][0])
        
    hist_data["energy"] = energy
    width = 20
    delim='\t'
    column1 = '-'
    order = ['energy', 'counts']
    
    with open( filepath, 'w' ) as f:
        writer, w = csv.writer(f, delimiter=delim), []
        head = ['{!s:{}}'.format(column1,width)]
        
        for i in order:    
            head.append('{!s:{}}'.format(i,width))
            
        writer.writerow(head)            
        
        for i in range(len(tupleenergy)):
            row = ['{!s:{}}'.format(i,width)]
            for k in order:
                temp = hist_data[k][i]
                row.append('{!s:{}}'.format(temp,width))

            writer.writerow(row)
    
    return print("your file has been saved")

    # fmt = lambda s: '{!s:{}}'.format(s, width)
    # with open(filepath, 'w+') as f:
    #     writer = csv.writer(f, delimiter=delim)
    #     writer.writerow([fmt(column1)] + [fmt(s) for s in order])
        
    #     for i in sorted(hist_data.keys()):
    #       row = []
    #       #row = ['{!s:{}}'.format(i,width)]
    #       for k in order: row.append('{!s:{}}'.format(hist_data[i][k],width))
    #       writer.writerow(row)
    
    # return print("your file has been saved")
    

def peakposition(x):
    peaks, _ = find_peaks(x, prominence=10)
    
    plt.plot(peaks, x[peaks], "xr"); plt.plot(x)
    plt.yscale('log')
    plt.show()
    return peaks

def save_data(data):
    save_path = input("Enter the path of the save folder: ")
    fname = input("enter the file name: ")
    fname = fname + ".txt"
    complete_path = os.path.join(save_path, fname)
    
    ch1 = data['ch1']
    ch2 = data['ch2']
    ch3 = data['ch3']
    ch4 = data['ch4']
    
    ch1 = json.dumps(ch1)
    ch2 = json.dumps(ch2)
    ch3 = json.dumps(ch3)
    ch4 = json.dumps(ch4)
    
    f = open(complete_path, "w+")
    f.write(ch1)
    f.write(ch2)
    f.write(ch3)
    f.write(ch4)
    
    f.close()
######################################################################################################################################################################################
######################################################################################################################################################################################
######################################################################################################################################################################################

# dir_input = input("Enter the directory of your File: ")
# filename = input("Enter the name of the file (with .bin): ")

# filepath = "{}{}{}".format(dir_input, os.sep, filename)
# filepath = os.sep.join([dir_input, filename])

filepath = 'C:/Users/admin/Desktop/pydrs4/tests/2channels.bin'
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

                
                baseline = 34000
                
                data_corr = -np.array(temp_data['data'])+2*baseline
                maxcounts = maxvalue(data_corr)
                
                hist_data = histogram(maxcounts, bins, title, 'channel')
                
                save = input("Do you want to save the plot and data of the histogram?  'yes' or 'no': ")
                
                if save == 'yes':
                    savehistogram(hist_data)
                    
                else:
                    operations = ['histogram', 'save_data', 'save_hist', 'next_channel', 'finish']
                    print("Caution: If next_channel or finish are selected current data can be overwritten and data might be lost!")
                    print("Available operations: ", operations)
                    command = input("choose an operation: ")
                    
            elif command == 'save_data':
                print('you chose save_data')
                save_data(data)
                
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
    
    



