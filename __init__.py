'''
Author: Nuno Amaro -  R&D NESTER
Description: Implementation of first services related to BDO Pilot 4
Assumptions: Reads 2 CSV files with specific formats from the project data folder and uses that data.
             Data is related to wave characteristics (significant height -> Hs and mean period -> Tm) of MARETEC 
             numerical model for locations of two buoys.
'''


#from netCDF4 import Dataset
import csv
#import itertools
import numpy as np
import matplotlib.pyplot as plt
import math
import scipy.stats as s
from datetime import datetime
#import pandas as pd

######################### READ DATA FROM CSV FILES INTO LISTS FOR EASIER HANDLING ############################
# CSV FORMAT: date_time,Monican01 Buoy model,date_time,Monican02 Buoy model
with open('mean_wave_period_10012014_29112017.csv', 'rb') as f:
    reader = csv.reader(f)
    list_mean_wave_periods = list(reader)  

with open('significant_wave_height_10012014_29112017.csv', 'rb') as f:
    reader = csv.reader(f)
    list_sign_wave_heights = list(reader)
   
list_sign_wave_heights.pop(0)#eliminate first line of CSV
list_mean_wave_periods.pop(0)#eliminate first line of CSV

wave_sign_height_B1 = [float(t[1]) for t in list_sign_wave_heights]
wave_sign_height_B2 = [float(t[3]) for t in list_sign_wave_heights]
wave_mean_period_B1 = [float(t[1]) for t in list_mean_wave_periods]
wave_mean_period_B2 = [float(t[3]) for t in list_mean_wave_periods]

#date and time are the same for both CSV's
#str example: "2017-11-13 1:0"
#Converts string into datetime object
date_time_str = [t[0] for t in list_sign_wave_heights] #creates a string of date/time
date_time = []
for i in range(len(date_time_str)):
    date_time.append(datetime.strptime(date_time_str[i],'%Y-%m-%d %H:%M'))
###########################################################################

heights = wave_sign_height_B1 #consider values of a Buoys for calculation
periods = wave_mean_period_B1

######################### BASIC STATISTICS #################################
number_readings = len(heights)#total number of readings

max_height = max(heights) # max wave height registered
max_period = max(periods) # max wave period registered
av_height = np.mean(heights) # average wave height
av_period = np.mean(periods) # average wave period
stand_dev_height = np.std(heights) # standard deviation of wave height
stand_dev_period = np.std(periods) # standard deviation of wave period
###########################################################################

######################### CREATE 2D HISTOGRAM WITH % OF OCCURRENCE OF SEA STATES FOR A BUOY #############################

max_x = math.ceil(max(heights))#finds the maximum values so that graphs scales are properly drawn
max_y = math.ceil(max(periods))

##draws the 2D Histogram (minimum values drawn: 0.5% of occurrences) and returns:
#counts -> tuple with matrix of % of each pair of occurrence (Wave Significant Height (Hs), Wave Mean Period (Tm)). Zero is defined as NaN
#xedges -> points of X scale
#yedges -> points of Y scale
#Image  -> figure 
counts, xedges, yedges, Image = plt.hist2d(heights, periods, (2*max_x, 2*max_y), 
                                           range=np.array([(0, max_x), (0, max_y)]), 
                                           cmap='YlOrRd', normed=True, cmin=0.005)

##Prints in the image the % of occurrence of each one of pairs (Hs,Tm)
dx = xedges[2]-xedges[1]
dy = yedges[2]-yedges[1]
for i in range(xedges.size-1):
    for j in range(yedges.size-1):
        xb = xedges[i] + 0.25*dx
        yb = yedges[j] + 0.25*dy
        val = 100.*counts[i,j]
        if math.isnan(val) == False:
            num = np.round(val,2)
            if num != 0 and num:
                plt.text(xb, yb, str(num), fontsize=6 )
cbar = plt.colorbar()
cbar.ax.set_ylabel('Probability of occurrence')
plt.xlabel('Wave Significant Height [m]')
plt.ylabel('Wave Mean Period [s]')

plt.show()

######################################################################################

######################### CALCULATION OF AVAILABLE POWER OUTPUT (AND STATISTICS) AND PLOT ITS HISTOGRAM, CALC OF ENERGY #############################
# P = 0.49 * Hs^2 * Tm

power_mat = []
for i in range(number_readings):
    power_mat.append(0.49*heights[i]*heights[i]*periods[i])

av_power = np.mean(power_mat) #Mean power available
max_power = max(power_mat) #Maximum power available
min_power = min(power_mat) #Minimum power available

energy = sum(power_mat) #total energy during the considered period
#print energy

plt.hist(power_mat, int(max_power), density=True) #plots power output histogram
plt.xlabel('Power Output [kW/m]')
plt.ylabel('Verified Occurrences')

plt.show()

plt.plot(date_time, power_mat)
plt.xlabel('Date')
plt.ylabel('Power Output [kW/m]')
plt.show()
#####################################################################################################################################################

######################### CREATION OF TIME-SERIES GRAPH FOR ONE VARIABLE #############################
plt.plot(date_time, periods)
plt.xlabel('Date')
plt.ylabel('Wave Mean Period [s]')
plt.show()

'''
#example: period of 1 year
test = []
test_time = []
for i in range(len(periods)): 
    if i < 7860:
        test.append(periods[i])
        test_time.append(date_time[i])

plt.plot(test_time, test)
plt.xlabel('Date')
plt.ylabel('Wave Mean Period [s]')
plt.show()
'''
######################################################################################################
print "exit"
