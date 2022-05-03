# -*- coding: utf-8 -*-
"""
Created on Sun Nov 14 19:05:20 2021
@author: Vicky Chen
This Code appl
"""

import matplotlib.pyplot as plt
from drs4 import DRS4BinaryFile
import numpy as np
from scipy.signal import find_peaks
import sys
import os
import csv

def welcomemsg(f):
    print("Welcome!")
    totalboards = f.num_boards
    board_channels = getboardchannel(f)
    print("You have connected ", totalboards, 
          "Board(s) with Channel(s)", board_channels )
    return None




    

def getboardID(f):
    boardID_list = f.board_ids
    
    ###this is only valid for the use of 1 Board only
    boardID = boardID_list[0]
    return boardID


def getboardchannel(f):
    boardID = getboardID(f)
    board_channels = f.channels[boardID]
    return board_channels
    

def extractdata(f):    
    i = 1
    boardID = getboardID(f)
    board_channels = f.channels[boardID]
    
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
        #Iterates through the lines of the binary file, Adds "stop" as default
        #value to stop the iteration at the end of the binary file
        event = next(f, "stop")
       
        if event == "stop":
            break
        
        else:
            #Getting the Datapoint of all 4 channels for the current line of
            #the binary file
            for i, channel in enumerate(board_channels):
                if channel == 1:
                    tempdata_list1.append(event.adc_data[boardID][channel]) 
                    list_length = len(tempdata_list1)
                    data_ID1.append(event.event_id)
                    data_time1.append(event.timestamp)                        
                    
                    data_ch1 = {
                        "data": tempdata_list1, 
                        "identity": data_ID1, 
                        "time": data_time1
                        } 
                    
                elif channel == 2:
                    tempdata_list2.append(event.adc_data[boardID][channel]) 
                    list_length = len(tempdata_list2)
                    data_ID2.append(event.event_id)
                    data_time2.append(event.timestamp)                        
                    
                    data_ch2 = {
                        "data": tempdata_list2, 
                        "identity": data_ID2, 
                        "time": data_time2
                        } 
                    
                elif channel == 3:
                    tempdata_list3.append(event.adc_data[boardID][channel]) 
                    list_length = len(tempdata_list3)
                    data_ID3.append(event.event_id)
                    data_time3.append(event.timestamp)                        
                    
                    data_ch3 = {
                        "data": tempdata_list3, 
                        "identity": data_ID3, 
                        "time": data_time3
                        }                 
                    
                elif channel == 4:
                    tempdata_list4.append(event.adc_data[boardID][channel])
                    list_length = len(tempdata_list4)
                    data_ID4.append(event.event_id)
                    data_time4.append(event.timestamp)                        
                    
                    data_ch4 = {
                        "data": tempdata_list4, 
                        "identity": data_ID4, 
                        "time": data_time4
                        }                 
                    
            #Saving the data of all 4 channels into one dictionary                
            data = {
                "ch1": data_ch1, 
                "ch2": data_ch2, 
                "ch3": data_ch3, 
                "ch4": data_ch4
                }         
               
    return data
            

#This function finds the maximum of the 1024 cells of each data point
def maxvalue(temp_data):
    baseline = 34000
    temp_data_int = temp_data['data']
    data_corr = -np.array(temp_data_int)+2*baseline
    maxcounts = []
    for i in range(len(data_corr)):
        maxvalue = np.amax(data_corr[i])
        maxcounts.append(maxvalue)
        
    maxcounts_keV = keVconversion(maxcounts)
    return maxcounts_keV

def keVconversion (maxcounts):
    slope = 759/13538.32
    intercept = -5634.612
    maxcounts_keV = [(maxcounts[i]*slope + intercept) 
                     for i in range(len(maxcounts))]
    
    return maxcounts_keV
    
#finds the peaks of the historam so you can match it with te spectrum
#of your source and calculate the conversion to keV

def findpeaks(maxcounts): 
    
    plt.xlabel("Energy")
    plt.ylabel("Counts")
    plt.hist(maxcounts[::-1],bins=300)
    ax = plt.gca()
    p = ax.patches
    plt.yscale('log')
    
    energy = [patch.get_xy() for patch in p]
    for i in range(len(energy)):
        temp_tuple = energy[i]
        temp_float = temp_tuple[0]
        
        energy[i] = temp_float
        
    arr_energy = np.array(energy)    
    counts = [patch.get_height() for patch in p]
    arr_counts = np.array(counts)
    hist_data = {"energy": arr_energy, "counts": arr_counts}

    #plt.show()
    
    peaks, _ = find_peaks(arr_counts, prominence=40)
    plt.plot(arr_energy[peaks], arr_counts[peaks], "xr")
    plt.hist(maxcounts[::-1],bins=300)
    plt.yscale('log')
    #plt.show()
    
    return peaks

def histogramtotxt(hist_data, filepath):
    width = 20
    delim='\t'
    column1 = '-'
    order = ['energy', 'counts']
    len_data = len(hist_data["counts"])
    with open( filepath, 'w' ) as f:
        writer, w = csv.writer(f, delimiter=delim), []
        head = ['{!s:{}}'.format(column1,width)]
        
        for i in order:    
            head.append('{!s:{}}'.format(i,width))
            
        writer.writerow(head)            
        
        for i in range(len_data):
            row = ['{!s:{}}'.format(i,width)]
            for k in order:
                temp = hist_data[k][i]
                row.append('{!s:{}}'.format(temp,width))
    
            writer.writerow(row)
    
    print("your data has been saved! ")
    
 

#Plots the data into a histogram with the option to save the plot and
#data of the histogram

def histogram(data, selected_channel):
    maxcounts = getchanneldata(data, selected_channel)
    title = input("choose a title for your plot: ")
    bins = int(input("choose the number of binaries: "))
    
    save = input("Do you want to save the plot and data of the histogram? "
                 + "'yes' or 'no': ")

    
    if save == 'yes':
        filepath = getfilepath()

        
    
    #creating histogram
    plt.title(title)
    plt.xlabel("Energy [keV]")
    plt.ylabel("Counts")
    #plt.hist(maxcounts[::-1],bins=bins)
    plt.hist(maxcounts,bins=bins)

    ax = plt.gca()
    p = ax.patches
    plt.yscale('log')
    
    #extracting data from histogram
    energy = [patch.get_xy() for patch in p]
    for i in range(len(energy)):
        temp_tuple = energy[i]
        temp_float = temp_tuple[0]
        
        energy[i] = temp_float
        
    arr_energy = np.array(energy)    
    counts = [patch.get_height() for patch in p]
    arr_counts = np.array(counts)    
    
    hist_data = {"energy": arr_energy, "counts": arr_counts}
    
    if save == 'yes':  
        
        #Saving the Plot as a .png
        path_png = filepath + ".png"
        plt.savefig(path_png)
        plt.show()
        
    
        #Saving the histogram data to a text file  
        path_txt = filepath + ".txt"
        histogramtotxt(hist_data, path_txt)
        
    else: plt.show();

        
        
    return hist_data


#Saving the data of one channel into a text file
#instead of saving all 1024 count of each data point only the maximum will 
#be saved for each data point

def save_data(data, selected_channel):
    
    filepath = getfilepath()  
    path_txt = filepath + ".txt"
    
    maxcounts = getchanneldata(data, selected_channel)
    
    data = data[selected_channel]
    
    temp =  {
        "maxcounts":
        "identity"
        "timestamp"
        }
    data["data"] = maxcounts
    
    temp["maxcounts"] = data["data"]
    temp["identity"] = data["identity"]
    temp["timestamp"] = data["time"]
    
    data = temp
    
    width = 20
    delim='\t'
    column1 = selected_channel
    order = ['maxcounts', 'identity', 'timestamp']
    
    with open( path_txt, 'w' ) as f:
        writer, w = csv.writer(f, delimiter=delim), []
        head = ['{!s:{}}'.format(column1,width)]
        
        for i in order:    
            head.append('{!s:{}}'.format(i,width))
            
        writer.writerow(head)            
        
        for i in range(len(data["identity"])):
            row = ['{!s:{}}'.format(i,width)]
            for k in order:
                temp = data[k][i]
                row.append('{!s:{}}'.format(temp,width))
    
            writer.writerow(row)
    
    print("your data has been saved! ")
    return None


def select_channel():
    selected_channel = input("Choose between 'ch1','ch2','ch3','ch4': ")
    print("You have selected channel: ", selected_channel)
    return selected_channel

def getchanneldata(data, selected_channel):
    temp_data = data[selected_channel]
    maxcounts = maxvalue(temp_data)
    return maxcounts

def select_operation():
    selected_channel = select_channel()
    x=1
    while x == 1:
        operations = ['histogram', 'save data', 'select channel', 'finish']
        print("Caution: If next_channel or finish are selected current "
              + "data can be overwritten and data might be lost!")
        print("Available operations: ", operations)
        command = input("choose an operation: ")
        
        if command == 'select channel':
            print('you chose select channel')
            select_channel()
            break     
        
        elif command == 'histogram':
            print('you chose histogram')
            histogram(data, selected_channel)
            
        elif command == 'save data':
            print('you chose save_data')
            save_data(data, selected_channel)
            
        elif command == 'finish':
            print('the program will be closed')   
            break
            
        else:
            print("invalid syntax")

def getfilepath(): 
    dir_input = input("Enter the directory of your File: ")
    filename = input("Enter the name of the file (with .*): ")
    filepath = "{}{}{}".format(dir_input, os.sep, filename)
    filepath = os.sep.join([dir_input, filename])      
    return filepath
    
##############################################################################    
#End of function definition
##############################################################################

#If getting the directory through console input is desired, uncomment the
#following lines. Note: This has only been tested on windows
#filepath = getfilepath()

#Alternatively you can directly input your filepath in the following line
#Make sure to comment out this line if you wish to input your filepath
#through the console. The following line will otherwise overwrite the
#input filepath: NOTE: use / as seperators
filepath = 'C:/Users/Vicky/Desktop/PALS-DRS4-Pydrs-main/tests/2ch100k.bin'

#the filepath will be printed so you can check that the registered filepath
#is correct
print(filepath)

##############################################################################
#Opening the file
with DRS4BinaryFile(filepath) as f:
    

    
    
    # welcomemsg(f)
     data = extractdata(f)   
        

        
    # select_operation()
    
    
    



