# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 22:19:09 2016

@author: user
"""
# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import scipy
from scipy.integrate import odeint
from scipy import linspace
from scipy import array
import matplotlib.pyplot as plt
import numpy as np
#CONTINUOUS ABSORPTION
#COMPONENTS: 1. CO2 2.CH4 3.H2O
pt=101325 # (atm) #total pressure of the system-User defined
T= 300 #  (Kelvin) Temperature of the system-User defined
d=0.075 # (cm) diameter of column - User defined
area=0.25*scipy.pi*d*d #Area of cross section
Vgas=100.0 #(kmol/s) -User defined
Vliq=100.0 #(kmol/s) -User defined
n=10; #no of points -User defined
h=10.0 #(m) height of column  -User defined
dz=h/(n-1);
kla1=0.0007; kla2=0.0007; #overall mass transfer coefficient liquid side:-Ref-(NEUMANN SYSTEMS GROUP,INC.) 
kgaw=0.002; #overall mass transfer coefficients gas side :-Ref-(NEUMANN SYSTEMS GROUP,INC.) 
H1=2.97619; H2=72.325; #Henry's constants for CO2 and CH4 repectively :-Ref-COMPILATION OF HENRY'S LAW CONSTANTS FOR ORGANIC SPECIES BY ROLF SANDER
pwsat=133.3224*scipy.exp(18.3036-3816.44/(T-46.13)) #(Pa)
Gw=0; Gco2=0.5*Vgas; Gch4=0.5*Vgas;
Lw=1*Vliq; Lco2=0; Lch4=0;
e=1;e1=1;e2=1;e3=1;
d1=0.04494; d2=0.04474;d3=55.55; #densities of CO2, CH4 and H2O respectively
R=8.314 #
k=0;
#####Conversions into SI Units#########
def epid(y,h):
    dg1dz=[ (-kla1*area*((y[0]*pt/((H1*(y[0]+y[1]+y[2]))))-(d1*y[3])/(y[3]+y[4]+y[5]))),
                   -kla2*area*((y[1]*pt/((H2*(y[0]+y[1]+y[2]))))-(d2*y[4])/(y[3]+y[4]+y[5])),
                   -kgaw*area*(y[2]*pt/(((y[0]+y[1]+y[2])))-pwsat),
                   -kla1*area*((y[0]*pt/((H1*(y[0]+y[1]+y[2]))))-(d1*y[3])/(y[3]+y[4]+y[5])),
                   -kla2*area*((y[1]*pt/((H2*(y[0]+y[1]+y[2]))))-(d2*y[4])/(y[3]+y[4]+y[5])),
                   -kgaw*area*(y[2]*pt/(((y[0]+y[1]+y[2])))-pwsat)]
    return dg1dz
#def yinitial(a):
    #return array([.5,.5,0,a[0],a[1],a[2]])
a1=array([0.4,0.1,0.5])
t=linspace(0.0,2.0,10)
yinitial=[0.5,0.5,0,a1[0],a1[1],a1[2]]
y=odeint(epid,yinitial,t)
F1=array([abs(y[n-1,3]),abs(y[n-1,4]),abs(y[n-1,5]-100)])
#print F1

a2=array([0.2,0.2,0.6])
t=linspace(0.0,2.0,10)
yinitial=[0.5,0.5,0,a2[0],a2[1],a2[2]]
y=odeint(epid,yinitial,t)
F2=array([abs(y[n-1,3]),abs(y[n-1,4]),abs(y[n-1,5]-100)])
#print F2
    
while (e>0.0001):
    Gw=0; Gco2=0.5*Vgas; Gch4=0.5*Vgas;
    b1=np.multiply(a2-a1,F2)
    #print F2
    #print F1
    m1k=F2-F1
    a3=a2-np.divide(b1,m1k)
    #t=linspace(0.0,9.0,10.0)
    yinitial=([0.5,0.5,0,a3[0],a3[1],a3[2]])
    y=odeint(epid,yinitial,t)
    F3=([abs(y[n-1,3]),abs(y[n-1,4]),abs(y[n-1,5]-100)])
    #ans=a2
    F1=F2
    F2=F3
    a1=a2
    a2=a3
    e=max(F3[0],F3[1],F3[2])   
          
print a3
h=linspace(0,2,n)
y0=[0.5,0.5,0,a3[0],a3[1],a3[2]]
solu=odeint(epid,y0,h)      
       # epid_solve=odeint(epid,y0,h)
       
        
#e1=100-solu[n-1,5];
#if e1<0:
  #e1=-e1
#e2=solu[n-1,3]/Vliq;
#if e2<0:
  #e2=-e2
#e3=solu[n-1,4]/Vliq;
#if e3<0:
  #e3=-e3
#e=(e1+e2+e3)
#print e;
#k=k+1;
print solu[:,5];
print solu[:,4];
print solu[:,3];
print solu[:,2];
print solu[:,1];
print solu[:,0];
plt.plot(h,y[:,5],'r')
plt.show()
plt.plot(h,y[:,4],'r')
plt.show()
plt.plot(h,y[:,3],'r')
plt.show()
plt.plot(h,y[:,2],'r')
plt.show()
plt.plot(h,y[:,1],'r')
plt.show()
plt.plot(h,y[:,0],'r')
plt.show()



