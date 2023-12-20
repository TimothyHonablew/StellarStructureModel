#Name: Timothy Honablew
#Date: November 13th, 2023 CE
#Purpose: Solving the four ODES for stellar modeling.

import numpy as np
from scipy.integrate import odeint

from opacity import *
from energy import *
from density import *
from load1 import *
from load2 import *

#Constants
Mo = 1.9891 * 10**33            #Name: Solar mass                       Units: g
G = 6.67259 * 10**-8            #Name: Gravitational Constant           Units: cm^3 g^-1 s^-2
mH = 1.6733 * 10**-24           #Name: Mass of Hydrogen Atom            Units: g
k = 1.380658 * 10**-16          #Name: Boltzmann Constant               Units: erg K^-1
a = 7.5646 * 10**-15            #Name: Radiation Density Constant       Units: erg cm^-3 K^-4
c = 3 * 10**10                  #Name: Speed of Light                   Units: cm s^-1


#Establishing the starting mass, mass fractions, and other parameters of my model star
mass = 4.20 * Mo                #Units: g
X = 0.690                       #Units: N/A
Y = 0.260                       #Units: N/A
Z = 0.050                       #Units: N/A

mu = 4/(3 + 5*X)                #Units: N/A

#Creating a nabla function to calculate the temperature gradient to use for the energy transport equation
def nablaValue(m, Press, Temp, Lumin, rad, opacity):
    
    kappa = currentOpacity(Temp, rad);       #Name: Opacity
    opacity.append(kappa);

    nablaRad = 3/(16*np.pi*a*c*G) * Press*kappa/Temp**4 * Lumin/m;
    nablaAd = 0.4;
    
    if nablaRad < nablaAd and nablaRad > 0:
        nabla = nablaRad;
    else:
        nabla = nablaAd;
        
    return nabla;

#Creating a function to solve the four coupled ODEs
def solving(choice, diffs, masses):
    
    #Defining the values that are calculated from the written functions from earlier steps
    radius = [];
    pressure = [];
    temperature = [];
    luminosity = [];
    rho = 0;
    
    #Defining the values that need to be uploaded onto a table later. They are inserted where appropriate in the solving funciton
    density = [];
    eGeneration = [];
    opacity = [];
    adiabaticGrad = [];
    
    
    #The if-else statement to determine if we're starting from the center or surface
    if choice == 1:
        m = 0; 
        
        L, r, P, T = intialCenter(diffs[0], diffs[1], diffs[2], diffs[3]);
        
        luminosity.append(L);
        radius.append(r);
        pressure.append(P);
        temperature.append(T);
        
        rho = currentDensity(T, P);    #Name: Density
        density.append(rho);
        
    else:
        m = mass;
        
        L, r, P, T = intialSurface(diffs[0], diffs[1], diffs[2], diffs[3]);
        
        luminosity.append(L);
        radius.append(r);
        pressure.append(P);
        temperature.append(T);
        
        rho = 3*mass/(4*np.pi*r**2);   #Name: Density
        density.append(rho);

    #Since the values are always changing, this for loop will incremement through the mass array one mass at a time and add to the 
    #depenedent variable arrays one at a time, to be able to use updated values of radius, pressure, temperature, and luminosity. The
    #temp array holds the current dependent values so they can be appended to the appropriate arrays with out adding in the previous 
    #value an additional time.
    
    for i in range(len(masses) - 1):
        
        #The current mass shell to be integrated
        currMass = (masses[i], masses[i+1]);
        
        #Appending density constantly so it is the same length as other arrays for ease of putting into a tbale
        density.append(rho);
        
        #The mass conservation differential eqauation
        def massCons(radius, m):
            dr = 1/(4 * np.pi * radius**2 * rho);
            return dr;
        
        temp = odeint(massCons, radius[i], currMass);
        radius.append(temp[1][0]);
        
        #The hydrostatic equilibrium differntial equation
        def hydroEq(P, m, radius):
            dP = -G * m/(4*np.pi*radius**4);
            return dP;
        
        temp = odeint(hydroEq, pressure[i], currMass, args = (radius[i+1],));
        pressure.append(temp[1][0])
        
        #The energy transport differential equation
        def energyTrans(Temp, m, Lumin, rad, Press, t):
            adiabaticGrad.append(nablaValue(currMass[1], Press, t, Lumin, rad, opacity));
            dT = -G * m * Temp * nablaValue(currMass[1], Press, t, Lumin, rad, opacity) * 1/(4*np.pi* rad**4 * Press);
            return dT;

        temp = odeint(energyTrans, temperature[i], currMass, args = (luminosity[i], radius[i+1], pressure[i+1], temperature[i],));
        temperature.append(temp[1][0]);

        #The energy generation differential equation
        def energyGen(Lumin, m, Temp):
            eGeneration.append(energyGeneration(Temp, rho));
            dL = energyGeneration(Temp, rho);
            return dL;
        
        temp = odeint(energyGen, luminosity[i], currMass, args = (temperature[i+1],));
        luminosity.append(temp[1][0]);
            
    
    return radius, pressure, temperature, luminosity, density, eGeneration, opacity, adiabaticGrad;
