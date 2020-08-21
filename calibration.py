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
        These parameters are also displayed to screen    
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
    
    print('Optimum: ', round(theta_all[-1][0], 12), round(theta_all[-1][1], 12), round(theta_all[-1][2], 12), round(theta_all[-1][3], 12))
    #print('Number of iterations needed: ', N_it)
    return theta_all[-1], obj(t0, t1, dt, x0, theta_all[-1])

if __name__ == "__main__":
    #GUESS INITIAL PARAMETERS - THEN APPLY GRADIENT DESCENT
    from random import seed, random
    from time import time

    seed(1)
    
    t0=1980
    t1=2016
    dt=1
    p_start=0.0313
    theta0=np.array([0.0001,0.0001,-0.05,0.05])
    theta_start, s_start=pressure_params(t0, t1, dt, p_start, theta0)

    for i in range(30):
        a=-0.1+random()*0.2
        b=-0.1+random()*0.2
        #Since pressures unlikely to be above/below +-0.05MPa
        p0=-0.05+random()*0.1 
        p1=-0.05+random()*0.1

        theta0=np.array([a,b,p0,p1])
        good_theta, good_s=pressure_params(t0, t1, dt, p_start, theta0)

        if (good_s<s_start):
            s_start=good_s

    print("Optimum obj value:", s_start)
    print("Optimum theta:",good_theta)    

