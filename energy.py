#Name: Timothy Honablew
#Date: November 13th, 2023 CE
#Purpose: Calculating the rate of energy generation for the 1D stellar model project. This was calculated from equations 18.63 and 18.65
#         from the Stellar Structure and Evolution textbook.

import numpy as np
from density import *

def energyGeneration(temperature, density):
    #Creating the variables that will be used in the energy generation equations except the weak screening effect

    X = 0.690;                   #Name: H Mass Fraction      Units: N/A
    Z = 0.050;                   #Name: Metal Mass Fraction  Units: N/A
    T9 = temperature;            #Name: Temperature          Units: 10**9 K
    rho = density;               #Name: Density              Units: g^1 cm^-3
    e = 4.803 * 10**-10;         #Name: Electron Charge      Units: esu
    
    #Calculating the values used in the energy generation equations
    psi = (2);
    g11 = (1 + 3.82*T9 + 1.51*T9**2 + 0.144*T9**3 - 0.0114*T9**4);
    g141 = (1 - 2.00*T9 + 3.41*T9**2 -2.43*T9**3);
    
    #Calculating the weak screening effect
    Zp = 1;         #Name: Charge Number of Proton
    xi = 1;
    f11 = (np.exp(5.92*10**-3 * Zp * Zp * (xi*rho/(100*T9)**3)**0.5));

    #Calculating all the energy generation rates
    epp = (2.57 * 10**4 * psi * f11 * g11 * rho * X**2 * T9**(-2/3) * np.exp(-3.381/T9**(1/3)));
    ecno = (8.24 * 10**25 * g141 * Z * X * rho * T9**(-2/3) * np.exp(-15.231*T9**(-1/3) - (T9/0.8)**2));

    etotal = (epp + ecno);
    
    return etotal;

        