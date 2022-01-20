# -*- coding: utf-8 -*-
"""
Created on Sun Nov 14 19:05:20 2021

@author: Vicky Chen
"""

import matplotlib.pyplot as plt
from drs4 import DRS4BinaryFile
import numpy as np
from scipy.signal import find_peaks

def getfilepath(path):
    filepath = path
    return filepath


def extractdata(f):    
    i = 1
    tempdata_list = []  
    data_ID = []
    data_time = []
    data = []
    
    boardID_list = f.board_ids
    boardID = boardID_list[0]
    totalBoards = len(boardID_list)
    boardID = boardID_list[0]

    boardCH = f.channels[boardID]
    print("You have connected ", totalBoards, "Board(s) with Channel(s)", boardCH )
   
    for x in range(len(boardCH)):
        channel = boardCH[x]      
                         
        while i == 1:    
            event = next(f, "stop")
            if event == "stop":                
                break
            
            else:
                tempdata_list.append(event.adc_data[boardID][1]) #event.adc_data[boardID][boardChannel] -> Board nr. 3059 mit Input auf Channel 1
                list_length = len(tempdata_list)
                data_ID.append(event.event_id)
                data_time.append(event.timestamp)
            
            channeldata = {"data": tempdata_list, "identity": data_ID, "time": data_time} 
            # plt.plot(event.adc_data[boardID][channel])
            # plt.show()           
            
        data.append(channeldata)      
                
    return data
            

            
def maxvalue(data):
    maxima = []
    for i in range(len(data)):
        minvalue = np.amax(data[i])
        maxima.append(minvalue)
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
def peakposition(x):
    peaks, _ = find_peaks(x, prominence=10)
    
    plt.plot(peaks, x[peaks], "xr"); plt.plot(x)
    plt.yscale('log')
    plt.show()
    return peaks


######################################################################################################################################################################################
######################################################################################################################################################################################
######################################################################################################################################################################################

filepath = 'C:/Users/admin/Desktop/pydrs4/tests/2channels.bin'

with DRS4BinaryFile(filepath) as f:
    
    print(f.board_ids)
    print(f.channels)
    data = extractdata(f)



tempdata_list1 = data[0]["data"]
tempdata_list2 = data[1]["data"]
baseline = 34000
tempdata_list1 = -np.array(tempdata_list1)+2*baseline
tempdata_list2 = -np.array(tempdata_list2)+2*baseline
tempdata_list1.tolist()
tempdata_list2.tolist()

maxcounts1 = maxvalue(tempdata_list1)
maxenergy = scaleaxis(maxcounts1)


maxima2 = maxvalue(tempdata_list2)

hist_data1 = histogram(maxcounts1, 230, 'CeBr3 Channel 1', 'channel')
hist_data1 = histogram(maxenergy, 230, 'CeBr3 Channel 1', 'Energy [keV]')

histogram(maxima2, 230, 'CeBr3 Channel 2', 'Channel')

energie = hist_data1['energy']

x = hist_data1['counts']
x = np.asarray(x)
peaks = peakposition(x)

# peaks = find_peaks(x, prominence=1)
# plt.plot(peaks, x[peaks], "xr"); plt.plot(x)


#plt.plot(tempdata_list[107]) #zeigt den 108. Messwert an
#plt.show()   



# histogram(maxima, bins, title)
# histogram = gethist(maxima, 150)
# hist_counts = histogram[0]
# hist_bins = histogram[1]


# plt.plot(hihist_counts)
#plt.plot(maxima)
#peak = peakposition(data)


