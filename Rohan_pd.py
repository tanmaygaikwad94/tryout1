# -*- coding: utf-8 -*-
"""
Created on Mon Feb 08 21:20:06 2016

@author: Hp
"""

import scipy
from scipy.stats import chisquare
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats.distributions import t
import pandas as pd
##Data fitting for vacuum drying data##
data=pd.read_excel("M1.xlsx","Sheet1")

xdata=scipy.array(data["Time(s)"])
ydata=scipy.array(data["X"])
xerror=scipy.array(data["de"])
print 'Time. = ' ,xdata 
print 'Moisturecontent = ' , ydata
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
tval=t.ppf(1.0-alpha/2.0, dof)
for i,p,var in zip(range(n),pars,np.diag(pcov)):
    sigma=var**0.5
    print  '[parameter1:; Value [Value-sigma, Value + sigma]' 
    print 'p{0};{1}[{2} {3}]\n'.format(i,p,p-sigma*tval,p+sigma*tval)
print 'sigma = ',sigma; print '\n'
print 'parameters value (a,b)=' ,pars; print '\n'
print 'Covariance= ', pcov ; print '\n'
#print 'fitted ydata= ' ,yfit; print '\n'

plt.plot(xdata,ydata,'*')  
#plt.plot(xdata,yerr,'o') 
yfit=func(xdata,pars[0],pars[1])
#print 'The following plot represents yfit vs xdata with solid line and ydata vs xdata with dots'
plt.plot(xdata,yfit,'r-')
plt.show()
#print 'The following plot shows variation of Error with Volume'
#plt.plot(delH,xerror,'*')
#plt.plot(delH,xerror,'--')
#plt.show()

