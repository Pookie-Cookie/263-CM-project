# ENGSCI263: Gradient Descent Calibration
# main.py

# PURPOSE:
# To IMPLEMENT and TEST a gradient descent calibration method.

# PREPARATION:
# Notebook calibration.ipynb.

# SUBMISSION:
# Show the instructor that you can produce the final figure in the lab document.

# import modules and functions
import numpy as np
from gradient_descent import obj_dir,step,line_search

# for improving gradient descent through random start-point generation
from random import seed, random
from time import time

# import pressure residual function as objective function to test
from gradient_descent import pressure_obj as obj



def pressure_params(t0, t1, dt, x0, theta0):
    ''' Obtains the minimum-residual parameters for the pressure lpm

        Parameters:
        -----------
        t0 : float
            Initial time of solution.
        t1 : float
            Final time of solution.
        dt : float
            Time step length.
        x0 : float
            Initial value of solution.
        theta0 : array-like
            Initial guess for 'good' parameters

        Returns:
        --------
        theta : array-like
            Vector of parameters for which the pressure lpm has a minimum regression from the data

        Notes:
        ------
        Parameters are evelauted through a gradient descent method.
        theta contains the parameters, in order : a, b, p0, p1   
    '''
    
    # compute steepest descent direction
    s0 = obj_dir(obj, t0, t1, dt, x0, theta0)

    # choose step size 
    alpha = 1.e-4
    
    # The following script repeats the process until an optimum is reached, or until the maximum number of iterations allowed is reached
    theta_all = [theta0]
    s_all = [s0]
    # iteration control
    N_max = 500
    N_it = 0
    
    #control variable - when to stop iterating ?
    iterate=True
    
    while iterate :
        # uncomment line below to implement line search
        #alpha = line_search(obj, t0, t1, dt, x0, theta_all[-1], s_all[-1])

        # update parameter vector 
        theta_next = step(theta0,s0,alpha)
        theta_all.append(theta_next) 	# save parameter value for plotting        
        
        # compute new direction for line search (thetas[-1]
        # **uncomment and complete the command below**
        s_next = obj_dir(obj, t0, t1, dt, x0, theta_next)
        s_all.append(s_next) 			# save search direction for plotting
        
        #if  objective function starts increasing then stop
        if abs((obj(t0, t1, dt, x0, theta_next)-obj(t0, t1, dt, x0, theta0)))<1.e-3:
            iterate=False
        elif N_it>N_max:
            iterate=False
        else:
            iterate=True         

        # compute magnitude of steepest descent direction for exit criteria
        N_it += 1
        # restart next iteration with values at end of previous iteration
        theta0 = 1.*theta_next
        s0 = 1.*s_next
    
    #print('Optimum: ', round(theta_all[-1][0], 12), round(theta_all[-1][1], 12), round(theta_all[-1][2], 12), round(theta_all[-1][3], 12))
    #print('Number of iterations needed: ', N_it)
    return theta_all[-1], obj(t0, t1, dt, x0, theta_all[-1])

def rand_pressure_params(n, t0, t1, dt, x0):
    ''' Uses randomly-generated parameters to improve accuracy of calibration
       
        Parameters:
        -----------
        n : int
            Number of gradient descent start points to test
        t0 : float
            Initial time of solution.
        t1 : float
            Final time of solution.
        dt : float
            Time step length.
        x0 : float
            Initial value of solution.

        Returns:
        --------
        theta_better : array-like
            Set of parameters for which pressure lpm objective function is lowest(of the start points tested)
        s_better : float
            Value of objective function for these parameters

        Notes:
        ------
        Random generation is set with a constant seed to ensure replicability
        Random generation for parameters p0, p1 is between 0.05 and -0.05
        and for a, b between -0.1 and 0.1. These ranges are based on data in ac_p.csv
        and on values obtained through ad-hoc calibration.
        n should be set to a value 40 or less to obtain parameters in a reasonable time.
    '''
    #keep seed const
    seed(1)
    #generate first starting pt params
    a=-0.1+random()*0.2
    b=-0.1+random()*0.2
    #Since pressures unlikely to be above/below +-0.05MPa
    p0=-0.05+random()*0.1 
    p1=-0.05+random()*0.1

    theta0=np.array([a,b,p0,p1])
    theta_start, s_start=pressure_params(t0, t1, dt, x0, theta0)

    for i in range(n):
        a=-0.1+random()*0.2
        b=-0.1+random()*0.2
        #Since pressures unlikely to be above/below +-0.05MPa
        p0=-0.05+random()*0.1 
        p1=-0.05+random()*0.1

        theta0=np.array([a,b,p0,p1])
        theta_better, s_better=pressure_params(t0, t1, dt, x0, theta0)

        if (s_better<s_start):
            s_start=s_better
            theta_start=theta_better
    
    return theta_start, s_start


