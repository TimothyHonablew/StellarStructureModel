# Name: Timothy Honablew
# Date: November 12th, 2023
# Purpose: This will check the error in the convergence of the two sets of ODES

import numpy as np

#This function returns the percent difference of what will be the middle point where the dependent functions meet and the percent
#difference is how much we will change the initial conditions by. So that the initial conditions don't change too much or veer 
#negative the percen they will be changed by is capped at 95%
def check(a, b):
    c = (np.abs(a-b))/a;
    
    if c > 1:
        c = 0.95;
        
    if a < b:
        c = -c;
        
    return c;
    
#This function checks if the percent differences are acceptable errors and we can conclude the program
def isDone(arr1, arr2, a):
    done = False;
    
    if(np.abs(arr1[0]) > a):
        done = True;
        
    if(np.abs(arr1[1]) > a):
        done = True;
        
    if(np.abs(arr1[2]) > a):
        done = True;
        
    if(np.abs(arr1[3]) > a):
        done = True;
        
    if(np.abs(arr2[0]) > a):
        done = True;
        
    if(np.abs(arr2[1]) > a):
        done = True;
        
    if(np.abs(arr2[2]) > a):
        done = True;
        
    if(np.abs(arr2[3]) > a):
        done = True;
        
    return done;