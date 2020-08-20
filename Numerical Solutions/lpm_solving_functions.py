#Contains numerical methods for solving lpm ODES
import numpy as np
from data_prep_functions import load_extraction_rates,interpolate_extraction

def solve_ode_pressure(f, t0, t1, dt, x0, pars):
    ''' Solve an ODE numerically for the Onehunga Aquifer system

        Parameters:
        -----------
        f : callable
            Function that returns dxdt given variable and parameter inputs.
        t0 : float
            Initial time of solution.
        t1 : float
            Final time of solution.
        dt : float
            Time step length.
        x0 : float
            Initial value of solution.
        pars : array-like
            List of parameters passed to ODE function f.

        Returns:
        --------
        t : array-like
            Independent variable solution vector.
        x : array-like
            Dependent variable solution vector.

        Notes:
        ------
        ODE is solved using the Improved Euler Method. 

        Assume that ODE function f takes the following inputs, in order:
            1. independent variable
            2. dependent variable
            3. forcing term, q
            4. all other parameters
    '''
	#initialise
	
    nt = int(np.ceil((t1-t0)/dt))		# compute number of Euler steps to take
    t = t0+np.arange(nt+1)*dt			# t array
    x = 0.*t							# array to store solution
    x[0] = x0							# set initial value
	
    #get values for the forcing term
    tv,qv=load_extraction_rates()
    q=interpolate_extraction(t,tv,qv)
    #q=np.zeros(len(t))
    #q.fill(1)

    for k in range(nt):
		#define forcing function q-VALUES FROM EXPERIMENT
        
        # k+1^th value of solution depends on k^th value of solution
		
        #find the slope at xk    
        dxdtk=f(t[k],x[k],q[k],*pars)
	    #increment solution by step size*derivative
        #to find a prediction of the solution at tk+h 
        xk1p=x[k]+dt*dxdtk
        
        #estimate the slope at xk1 using the prediction of xk1
        dxdtk1=f(t[k]+dt,xk1p,q[k],*pars)

        #Use the slope at xk1 to correct the prediction of xk1
        #using the average slope across xk and xk1
        x[k+1]=x[k]+0.5*dt*(dxdtk+dxdtk1)     


    return t,x