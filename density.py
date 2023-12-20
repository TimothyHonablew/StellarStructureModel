#Name: Timothy Honablew
#Date: November 13th, 2023 CE
#Purpose: Calculating the density of the model star based on pressure, temperature, and composition.

def currentDensity(temperature, pressure):
    
    #Creating the variables and constants to use in the pressure equaiton that will be rewritten for rho

    X = 0.690;                  #Name: H Mass Fraction                  Units: N/A                
    P = pressure;               #Name: Pressure                         Units: dyne cm^-2
    k = 1.381 * 10**-16;        #Name: Boltzmann Constant               Units: erg K^-1
    T = temperature;            #Name: Temperature                      Units: K
    mu = 4/(3 + 5*X);           #Name: Total Mean Molecular Weight      Units: N/A
    mH= 1.6733 * 10**-24;       #Name: Mass of Hydrogen Atom            Units: g
    a = 7.565 * 10**-15;        #Name: Radiation Density Constant       Units: erg cm^-3 K^-4
    
    rho = (mu * mH / k / T) * (P - 1/3 * a * T**4);
    return rho;
