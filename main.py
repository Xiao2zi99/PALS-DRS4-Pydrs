# -*- coding: utf-8 -*-
"""
Created on Sun Nov 14 19:05:20 2021

@author: Vicky Chen
"""

import matplotlib.pyplot as plt
from drs4 import DRS4BinaryFile
import numpy as np
from scipy.signal import find_peaks


def extractdata(f):    
    i = 1
    tempdata_list = []  
    data_ID = []
    data_time = []
    data = []
    
    boardID_list = f.board_ids
    totalBoards = len(boardID_list)
    boardID = boardID_list[0]

    boardCH = f.channels[3059]
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
def scaleaxis():
    
    return 0
###################################
def gethist(maxima, bins):
    hist_arr = np.histogram(maxima, bins=bins)
    return hist_arr

def plothistogram(maxima, bins, title):
    plt.title(title)
    plt.xlabel("Energie")
    plt.ylabel("Counts")
    plt.hist(maxima[::-1],bins=bins)
    plt.yscale('log')
    plt.show()
    return 0


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
maxima1 = maxvalue(tempdata_list1)
maxima2 = maxvalue(tempdata_list2)

plothistogram(maxima1, 150, 'CeBr3 Channel 1')
plothistogram(maxima2, 150, 'CeBr3 Channel 2')

#plt.plot(tempdata_list[107]) #zeigt den 108. Messwert an
#plt.show()   



# plothistogram(maxima, bins, title)
# histogram = gethist(maxima, 150)
# hist_counts = histogram[0]
# hist_bins = histogram[1]


# plt.plot(hihist_counts)
#plt.plot(maxima)
#peak = peakposition(data)


