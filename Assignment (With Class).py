
import pylab
from pylab import *
class Assignment:
                       #Given Data
    ma = 1.0
    mb = 2.0
    p = 10.0
    l = 10.0
    u = 100.0
    tain = 400.0
    tbin = 300.0
    nt=20
    def solve(self):
        ma =self.ma
        mb = self.mb
        p = self.p
        l = self.l
        u = self.u
        tain = self.tain
        tbin = self.tbin
        nt=self.nt
                       #Functions Used
        def temp(ma,mb,p,u,t):
            return array([-p*u*((t)[0]-(t)[1])/ma/(4000+0.1*(t)[0]+0.01*(t)[0]*(t)[0]),-p*u*((t)[0]-(t)[1])/mb/(3000+0.2*(t)[1]+0.05*(t)[1]*(t)[1])])
        
        def ha(t):
            return 4000*t+0.05*t*t+0.01/3*t**3
    
        def hb(t):
            return 3000*t+0.1*t*t+0.05/3*t**3


        e=pylab.zeros((nt-2,1)) #array for storing error values

        for n in range(2,nt):     #n is number of elements
   
            t1=pylab.zeros((n,2))
            t2=pylab.zeros((n,2))
    
            dx = l / n
    
            (t1[0])[0] = tain
            (t2[0])[0] = tain
            (t1[0])[1] = 326   #two guess for Tb,out
            (t2[0])[1] = 320
            e2 = 1
            while abs(e2) > 0.0000001:   #while loop to ensure error limit
        
                for i in range(0,n-1):
            
                    #forward difference used here
                    t1[i+1]=t1[i]+dx*temp(ma,mb,p,u,t1[i])
                    t2[i+1]=t2[i]+dx*temp(ma,mb,p,u,t2[i])

                       #shooting method using secant method
                e1 = tbin - (t1[n-1])[1]
                e2 = tbin - (t2[n-1])[1]
                (t2[0])[1] = (t2[0])[1] - ((t2[0])[1] - (t1[0])[1]) * e2 / (e2 - e1)


                      #Macroscopic Error Calculation
            dha = ma * (ha((t2[0])[0]) - ha((t2[n-1])[0])) #Cp dT integrals found out analytically
            dhb = mb * (hb((t2[0])[1]) - hb((t2[n-1])[1]))
                      #Value being added to error matrix   
            e[n-2]=([100*abs(dha-dhb)/dha])
        
        
                         #Plotting
        x=linspace(0,10,n)
        pylab.plot(x,t2) #Temp vs Distance
        pylab.show()
        n=range(2,nt)
        pylab.plot(n,e)  #Error vs number of points
        pylab.show()
        
                          
        
        

