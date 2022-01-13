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
    data_list = []  
    data_ID = []
    data_time = []
    while i == 1:    
        event = next(f, "stop")
        if event == "stop":
            break
        
        else:
            data_list.append(event.adc_data[3059][1]) #event.adc_data[boardID][boardChannel] -> Board nr. 3059 mit Input auf Channel 1
            list_length = len(data_list)
            data_ID.append(event.event_id)
            data_time.append(event.timestamp)
    dict_data = {"data": data_list, "identity": data_ID, "time": data_time}         
    return dict_data
            # 
            # 
            # plt.plot(event.adc_data[3059][1])
            # plt.show()
            
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


with DRS4BinaryFile('C:/Users/admin/Desktop/pydrs4/tests/2channels.bin') as f:
    
    print(f.board_ids)
    print(f.channels)
    dict_data = extractdata(f)
    
data_list = dict_data["data"]
baseline = 34000
data_list = -np.array(data_list)+2*baseline
data_list.tolist()
plt.plot(data_list[107])
plt.show()   
maxima = maxvalue(data_list)

# #plothistogram(maxima, 150, 'CeBr3')
# plothistogram(maxima, bins, title)
# histogram = gethist(maxima, 150)
# hist_counts = histogram[0]
# hist_bins = histogram[1]


# plt.plot(hihist_counts)
# #plt.plot(maxima)
# #peak = peakposition(data)


