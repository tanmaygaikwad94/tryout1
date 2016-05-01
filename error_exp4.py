# -*- coding: utf-8 -*-
"""
Created on Tue Feb 02 22:27:29 2016

@author: Hardik_2
"""

import scipy
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import win32com.client


xl=win32com.client.gencache.EnsureDispatch("Excel.Application")
wb=xl.Workbooks('13che1032exp4.xlsx')
sheet=wb.Sheets('tank')
def getdat(sheet,Range):
    data=sheet.Range(Range).Value
    data=scipy.array(data)
    data=data.reshape((1,len(data)))[0]
    return data
'''we have insered of data of dh and time for 1st order system for tank
performed in C.E. Lab'''
time=getdat(sheet,"H4:H37")#time scale
dh=getdat(sheet,"J4:J37") # change in height scale
n=len(time)# total number of observation

def dhvstime(time,a,b):
    return a*time/(1+b*time)
'''function is defined as dh=a*t/(1+b*t),assume a,b is constants which cab be
found from curve fitting'''
m=[1.0,2.0]#intial guess
cont,cov=curve_fit(dhvstime,time,dh,m)
a0=cont[0]#value of a
b0=cont[1]#valye of b
dhfitted=(a0*np.array(time))/(1+b0*np.array(time))#array to find fitted value

diffh=dhfitted-dh#array of difference between fitted and experimental

diffh2=diffh**2
moddiffh=diffh2**0.5# difference should be modei.e. should be positive.
print 'Sr.No','time   ','dh experi',' dh fitted    ','   dh exp-dh fitted'
for i in range (n):
    print '(',i+1,') ',time[i],'   ',dh[i],'    ',dhfitted[i],'     ',moddiffh[i]
averagedh=scipy.average(moddiffh)# to find mean
dhdavg=((np.array(averagedh))-moddiffh)**2# to find (x-xavg)^2
variance=(sum(dhdavg))/(n-1)# just found variance
sd=variance**0.5# standard deviation
print 'standard deviation: ', sd
error=(sum(((np.array(moddiffh)))**2))/variance
print 'variance: ',variance
error=sd/(n**0.5)
print 'error:',error

plt.plot(time,dh,'*')  
hfit=dhvstime(time,a0,b0)
plt.plot(time,hfit,'r-')
plt.show
