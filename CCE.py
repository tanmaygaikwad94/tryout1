# -*- coding: utf-8 -*-
"""
Created on Thu Jan 07 17:55:09 2016

@author: MEET SHAH
"""
import scipy
import pylab as plt
#CONTINUOUS CONTACTING EQUIPMENT
#COMPONENTS: 1. CO2 2.CH4 3.H2O
pt=int(input('Pressure of System (in atm)=')) # (atm) #total pressure of the system
T=int(input('Temperature of System (in Kelvin)=')) #  (Kelvin) Temperature of the system
d=7.5 # (cm) diameter of column 
area=0.25*scipy.pi*d*d*0.0001 #Area of cross section
Vgas=100.0000000 #(kmol/s) Inlet gas molar flow rate
Vliq=100.0000000#(kmol/s) Inlet liquid molar flow rate
n=100; #no of points
h=10.0 #(m) height of column
dz=h/(n-1);
kla1=0.0007; kla2=0.0005 ; kgaw=0.0002; #overall mass transfer coefficients
H1=10000.0/3.3; H2=100000.0/1.4; #(Pa m3/mol) Henry's constants for CO2 and CH4 repectively
pwsat=scipy.exp(18.3036-3816.44/(T-46.13)) #(mmhg)
Gw=0; Gco2=0.5*Vgas; Gch4=0.5*Vgas;
Lw=1*Vliq; Lco2=0; Lch4=0;
e=1;e1=1;e2=1;e3=1;
ro1=1.977/44.01; ro2=0.656/16.04;ro3=55.55; #(kmol/m3) molar densities of CO2, CH4 and H2O respectively
R=8.314 #
m=0;
dh=dz;
#####Conversions into SI Units#########
pt=pt*1.013*100000 #conversion into pascal
pwsat=pwsat*101325/760;#conversion into pascal
##Program Defining:
'''
Here error is defined as a product of three different errors each for co2,ch4 as well as H20 whereby we are 
adapting iterative procedure of minimising error product and incrementing guess variables in such a way that 
inlet liquid molar flow rate obtained after n iterations should be equal to 100 kmloes/sec for water, 0 kmoles/sec for co2 
as well as for ch4
'''
while e>0.0000000000001:
    Gw=0; Gco2=0.5*Vgas; Gch4=0.5*Vgas;
    if e2>0.00000001:
        Lco2=(0+m*0.01)*Vliq;
        L1=Lco2;
    if e3>0.0000001:
        Lch4=(0+m*0.001)*Vliq;
        L2=Lch4
    if e1>0.0001:
        Lw=1*Vliq-Lco2-Lch4;
        L3=Lw;
    for i in range(n):
        dg1dz=-kla1*area*((Gco2*pt/((H1*(Gw+Gco2+Gch4))))-(ro1*Lco2)/(Lw+Lco2+Lch4));
        Gco2=Gco2+dg1dz*dz;
        dg2dz=-kla2*area*((Gch4*pt/((H2*(Gw+Gco2+Gch4))))-(ro2*Lch4)/(Lw+Lco2+Lch4));
        Gch4=Gch4+dg2dz*dz;
        dg3dz=-kgaw*area*(Gw*pt/((R*T*(Gw+Gco2+Gch4)))-pwsat/(R*T))
        Gw=Gw+dg3dz*dz;
        dl1dz=-kla1*area*((Gco2*pt/((H1*(Gw+Gco2+Gch4))))-(ro1*Lco2)/(Lw+Lco2+Lch4));
        Lco2=Lco2-dl1dz*dz;
        dl2dz=-kla2*area*((Gch4*pt/((H2*(Gw+Gco2+Gch4))))-(ro2*Lch4)/(Lw+Lco2+Lch4));
        Lch4=Lch4-dl2dz*dz;
        h=h-dh;
        Lw=(Vliq+Vgas)-(Lco2+Lch4+Gco2+Gch4+Gw);
        plt.plot(h,Lco2,'ro')
    e1=100-Lw;
    if e1<0:
        e1=Lw-100;
    e2=Lco2/Vliq;
    e3=Lch4/Vliq;
    e=e1*e2*e3;
    print e1,e2,e3
    m=m+1;
print "All  molar flow rates are in kmol/sec"
print "Inlet Lw =" ,Lw 
print "Inlet Lco2=", Lco2 ;
print "Inlet Lch4=" ,Lch4;
print "Outlet Gw= ", Gw;
print "Outlet Gch4=" ,Gch4;
print "Outlet Gco2=" ,Gco2;
Lco2out=0.5*Vgas-Gco2;
print"Outlet Lco2 :Kmoles of co2 absorbed = ", Lco2out;
Lch4out=0.5*Vgas-Gch4;
print"Outlet Lch4 :Kmoles of ch4 absorbed =", Lch4out;
Lwout=100-Gw;
print "Outlet Lw  =" ,Lwout;
print "Kmoles of water vaporised =" ,Gw;
plt.show()

        
        
        
        
    
    