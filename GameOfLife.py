# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 20:39:43 2016

@author: MEET SHAH
"""

import scipy
from scipy import array
import numpy as np
m=int(input('Dimensions of Row='))
n=int(input('Dimensions of column='))
a=np.empty((m,n),dtype=int)
h=scipy.linspace(1,m-2,m-2)
k=scipy.linspace(1,n-2,n-2)
a[0,:]=0;a[m-1,:]=0;a[:,n-1]=0;a[:,0]=0;
for i in h:
    for j in k:
        a[i,j]=int(input('Enter Number 3='))
print a;
def bareearth(x,y):    # x:grass ; y:prey
    if x>=2:
        if y>=1:
            z=2;
    if x>0:
        z=1;
    else:
        z=0;
    return z;
def grass(x,y):     #x:prey ; y: predator
    if x>1:
        z=0;
    if x>=2:
        if y>=1:
            z=3;
    if y>0:
        z=2;
    else:
        z=1;
    return z
def prey(x,y):    # x:  grass ; y: predator
    if x<2:
        z=0;
    if y>1:
        z=1;
    else:
        z=2;
    return z;
def predator(x):   # x: prey
    if x<2:
        z=1;
    else:
        z=3;
    return z;
for v in range(5):
    for i in h:
        for j in k:
            gr=0;pr=0;pred=0;
            z=a[i,j];
            b=array([a[i-1,j-1],a[i-1,j],a[i-1,j],a[i,j-1],a[i,j+1],a[i+1,j-1],a[i+1,j],a[i+1,j+1]])
            for l in range(8):
                if b[l]==1:
                    gr=gr+1;
                if b[l]==2:
                    pr=pr+1;
                if b[l]==3:
                    pred=pred+1
            if z==0:
                a[i,j]=bareearth(gr,pr);
            if z==1:
                a[i,j]=grass(pr,pred);
            if z==2:
                a[i,j]=prey(gr,pred);
            if z==3:
               a[i,j]=predator(pr);
    print a;
        
