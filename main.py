# Name: Timothy Honablew
# Date: November 12th, 2023
# Purpose: The recursive program that will converg the two sets of ODES.

# Import Statements
import numpy as np
import math as m
from scipy.optimize import fsolve
from scipy.integrate import odeint

from matplotlib.axis import Axis
from matplotlib.ticker import AutoMinorLocator
import matplotlib.pyplot as plt
import xlwt

from opacity import *
from energy import *
from density import *
from load1 import *
from load2 import *
from diffEqSolver import *
from checker import *


#Constants
Mo = 1.9891 * 10**33            #Name: Solar mass                       Units: g
G = 6.67259 * 10**-8            #Name: Gravitational Constant           Units: cm^3 g^-1 s^-2
mH = 1.6733 * 10**-24           #Name: Mass of Hydrogen Atom            Units: g
k = 1.380658 * 10**-16          #Name: Boltzmann Constant               Units: erg K^-1
a = 7.5646 * 10**-15            #Name: Radiation Density Constant       Units: erg cm^-3 K^-4


#Establishing the starting mass, mass fractions, and other parameters of my model star
mass = 4.20 * Mo                #Units: g
X = 0.690                       #Units: N/A
Y = 0.260                       #Units: N/A
Z = 0.050                       #Units: N/A

mu = 4/(3 + 5*X)                #Units: N/A


#Creating the array of masses and percent differences
massCent = np.linspace(10**-5, mass/2, 100);
massSurf = np.linspace(mass, mass/2, 100);
diffsCenter = [0.15, 0.15, 0.15, 0.15];
diffsSurface = [0.15, 0.15, 0.15, 0.15];

finalIndex = len(massCent) - 1


#Creating the array to hold the dependent variables
radiusCenter =[];
pressureCenter = [];
temperatureCenter = [];
luminosityCenter = [];

radiusSurf =[];
pressureSurf = [];
temperatureSurf =[];
luminositySurf =[]; 

#Creating arrays to hold the data being input to the table
densityC = [];
densityS = [];

eGenC = [];
eGenS = [];

opacityC =[];
opacityS = [];

adGradC = [];
adGradS = [];

#Creating the loop to reach convergence or stop after too many tries
i = 1;
while(isDone(diffsCenter, diffsSurface, 0.1) and i < 100):
    
    radiusSurf, pressureSurf, temperatureSurf, luminositySurf, densityS, eGenS, opacityS, adGradS = solving(2, diffsSurface, massSurf);
    radiusCenter, pressureCenter, temperatureCenter, luminosityCenter, densityC, eGenC, opacityC, adGradC= solving(1, diffsCenter, massCent);

    diffsCenter[0] = check(luminosityCenter[finalIndex], luminositySurf[finalIndex]);
    diffsCenter[1] = check(radiusCenter[finalIndex], radiusSurf[finalIndex]);
    diffsCenter[2] = check(pressureCenter[finalIndex], pressureSurf[finalIndex]);
    diffsCenter[3] = check(temperatureCenter[finalIndex], temperatureSurf[finalIndex]);

    diffsSurface[0] = check(luminositySurf[finalIndex], luminosityCenter[finalIndex]);
    diffsSurface[1] = check(radiusSurf[finalIndex], radiusCenter[finalIndex]);
    diffsSurface[2] = check(pressureSurf[finalIndex], pressureCenter[finalIndex]);
    diffsSurface[3] = check(temperatureSurf[finalIndex], temperatureCenter[finalIndex]);

    i = i + 1;

#Calculating the actual temperature gradient by taking the derivative of ln(T) with respect to ln(P)
actualGradientCenter = [];
for i in range(len(temperatureCenter) - 1):
    tdiff = m.log(temperatureCenter[i+1]) - m.log(temperatureCenter[i])
    
    if pressureCenter[i+1] < 0 or pressureCenter[i] < 0:
        actualGradientCenter.append('nan')
    else:
        pdiff = m.log(pressureCenter[i+1]) - m.log(pressureCenter[i])
    
        if pdiff <= 0:
            actualGradientCenter.append('nan')
        else:
            actualGradientCenter.append(tdiff/pdiff)
actualGradientCenter.append(actualGradientCenter[len(actualGradientCenter) - 1])

actualGradientSurface = [];
for i in range(len(temperatureSurf) - 1):
    tdiff = m.log(temperatureSurf[i+1]) - m.log(temperatureSurf[i])
    
    if pressureSurf[i+1] < 0 or pressureSurf[i] < 0:
        actualGradientSurface.append('nan')
    else:
        pdiff = m.log(pressureSurf[i+1]) - m.log(pressureSurf[i])
    
        if pdiff <= 0:
            actualGradientSurface.append('nan')
        else:
            actualGradientSurface.append(tdiff/pdiff)
actualGradientSurface.append(actualGradientSurface[len(actualGradientSurface) - 1])


#Plotting the calculations
plt.subplot(221);
plt.plot(massCent, radiusCenter, 'red', label = 'From Center');
plt.plot(massSurf, radiusSurf, 'blue', label = 'From Surface');
plt.legend();
plt.xlabel("Mass (g)");
plt.ylabel("Radius (cm)");
plt.title('Stellar Radius as a Function of Mass');

plt.subplot(222);
plt.plot(massCent, pressureCenter, 'red', label = 'From Center');
plt.plot(massSurf, pressureSurf, 'blue', label = 'From Surface');
plt.legend();
plt.xlabel("Mass (g)");
plt.ylabel("Pressure (dyne cm^-2)");
plt.title('Stellar Pressure as a Function of Mass');

plt.subplot(223);
plt.plot(massCent, temperatureCenter, 'red', label = 'From Center');
plt.plot(massSurf, temperatureSurf, 'blue', label = 'From Surface');
plt.legend();
plt.xlabel("Mass (g)");
plt.ylabel("Temperature (K)");
plt.title('Stellar Temperature as a Function of Mass');

plt.subplot(224);
plt.plot(massCent, luminosityCenter, 'red', label = 'From Center');
plt.plot(massSurf, luminositySurf, 'blue', label = 'From Surface');
plt.legend();
plt.xlabel("Mass (g)");
plt.ylabel("Luminosity (erg s^-1)");
plt.title('Stellar Luminosity as a Function of Mass');



#Creating the table of all the requeseted data
book = xlwt.Workbook()

sheet1 = book.add_sheet("Sheet 1")

sheet1.write(0, 0, "Mass (g)")
sheet1.write(0, 1, "Radius (cm)")
sheet1.write(0, 2, "Density (g cm^-3)")
sheet1.write(0, 3, "Temperature (K)")
sheet1.write(0, 4, "Pressure (dyne cm^-2)")
sheet1.write(0, 5, "Luminosity (erg s^-1)")
sheet1.write(0, 6, "Energy Generation Rate (erg s^-1)")
sheet1.write(0, 7, "Opacity")
sheet1.write(0, 8, "Adiabatic Temperature Gradient")
sheet1.write(0, 9, "Real Temperature Gradient")
sheet1.write(0, 10, "Convective/Radiative Nature")

n = 0;
for n in range(len(massCent)):
    sheet1.write(n+1, 0, str(massCent[n]))
    sheet1.write(n+1, 1, str(radiusCenter[n]))
    sheet1.write(n+1, 2, str(densityC[n]))
    sheet1.write(n+1, 3, str(temperatureCenter[n]))
    sheet1.write(n+1, 4, str(pressureCenter[n]))
    sheet1.write(n+1, 5, str(luminosityCenter[n]))
    sheet1.write(n+1, 6, str(eGenC[n]))
    sheet1.write(n+1, 7, str(opacityC[n]))
    sheet1.write(n+1, 8, str(adGradC[n]))
    sheet1.write(n+1, 9, str(actualGradientCenter[n]))
    
    if not(type(actualGradientCenter[n]) is str) and actualGradientCenter[n] > adGradC[n]:
        sheet1.write(n+1, 10, 'Convective')
    else:
        sheet1.write(n+1, 10, 'Radiative')

maxIndex = len(massSurf) - 1
for p in range(len(massSurf)):
    sheet1.write(n+p+2, 0, str(massSurf[maxIndex - p]))
    sheet1.write(n+p+2, 1, str(radiusSurf[maxIndex - p]))
    sheet1.write(n+p+2, 2, str(densityS[maxIndex - p]))
    sheet1.write(n+p+2, 3, str(temperatureSurf[maxIndex - p]))
    sheet1.write(n+p+2, 4, str(pressureSurf[maxIndex - p]))
    sheet1.write(n+p+2, 5, str(luminositySurf[maxIndex - p]))
    sheet1.write(n+p+2, 6, str(eGenS[maxIndex - p]))
    sheet1.write(n+p+2, 7, str(opacityS[maxIndex - p]))
    sheet1.write(n+p+2, 8, str(adGradS[maxIndex - p]))
    sheet1.write(n+p+2, 9, str(actualGradientSurface[maxIndex - p]))
    
    if not(type(actualGradientCenter[maxIndex - p]) is str) and actualGradientSurface[maxIndex - p] > adGradS[maxIndex - p]:
        sheet1.write(n+p+2, 10, 'Convective')
    else:
        sheet1.write(n+p+2, 10, 'Radiative')

book.save("C://Users//thona//Downloads//Stellar Structure Project//Stellar Structure Model Table.xls")

plt.show();