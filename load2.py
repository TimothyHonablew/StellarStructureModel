#Name: Timothy Honablew
#Date: November 13th, 2023 CE
#Purpose: This code chooses the initial values of the dependent variables for the center of the star for the stellar model.

#Setting the intital guesses
L = 9 * 10**33;     #Name: Luminosty
r = 8 * 10**10;     #Name: Radius
P = 1;              #Name: Pressure
T = 1;              #Name: Temperature

#This functions changes the initial guesses by half of the calculated percent differences to try to reach convergence
def intialSurface(diffL, diffR, diffP, diffT):
    return L * (1 - diffL/2), r * (1-diffR/2), P * (1-diffP/2), T * (1-diffT/2);