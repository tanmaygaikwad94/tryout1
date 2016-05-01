# -*- coding: utf-8 -*-
"""
Created on Sat Apr 30 15:08:11 2016

@author: MEET SHAH
"""

import scipy
from scipy.integrate import odeint
from scipy.stats import chisquare
from scipy import linspace
from scipy import array
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from scipy.stats.distributions import t
data=pd.read_excel("data.xlsx","Sheet")
print data
'''
xl=win32com.client.gencache.EnsureDispatch("Excel.Application")
wb=xl.Workbooks('data.xlsx')
sheet=wb.Sheets('Sheet')
def getdat(sheet,Range):
    data=sheet.Range(Range).Value
    data=scipy.array(data)
    data=data.reshape((1,len(data)))[0]
    return data
xdata=getdat(sheet,"A2:A11")
R=getdat(sheet,"B2:B11")
P=getdat(sheet,"C2:C11")
print xdata
print R
print P
'''
xdata=scipy.array(data["Col1"])
ydata=scipy.array(data["Col2"])
k1=0.05
k2=0.05

def epid(y,h):
    dg1dz=[ (-k1*y[0]),(-k2*y[1])]
    return dg1dz
#def yinitial(a):
    #return array([.5,.5,0,a[0],a[1],a[2]])
yinitial=[0.5,0.4]
t=linspace(1.0,10.0,100.0)
y=odeint(epid,yinitial,t)
print y
print y[99,1]
def func(xdata,a,b):
    return a*scipy.exp(-b*xdata) ##Exponential data fitting
initial_guess=[1.0,0.01]
pars,pcov=curve_fit(func,xdata,ydata,p0=initial_guess)

#95%confidence interval
alpha=0.05
n=len(ydata) #number of data points
p=len(pars)  #number of parameters

dof=max(0,n-p)  #degree of freedom
def error(p,xdata,ydata):
    err=ydata-func(xdata,p)
    return err
def get_r2(xdata,ydata,yfit):
    ydatamean=scipy.average(ydata)
    dydatamean2=(ydata-ydatamean)**2
    dyfit2=(ydata-yfit)**2
    r2=1-sum(dyfit2)/sum(dydatamean2)
    return r2
#student-tvalue dor dof and confidence level

#plt.plot(xdata,yerr,'o') 
yfit=func(xdata,pars[0],pars[1])
print 'The following plot represents yfit vs xdata with solid line and ydata vs xdata with dots'
plt.plot(xdata,yfit,'g-')
plt.show()
print 'The following plot shows variation of Error with Volume'
print pars

