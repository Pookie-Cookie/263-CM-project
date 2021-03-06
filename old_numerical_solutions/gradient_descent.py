# ENGSCI263: Gradient Descent Calibration
# gradient_descent.py

# PURPOSE:
# IMPLEMENT gradient descent functions.

# PREPARATION:
# Notebook calibration.ipynb.

# SUBMISSION:
# Show the instructor that you can produce the final figure in the lab document.

# import modules
import numpy as np
from numpy.linalg import norm


# **this function is incomplete**
#					 ----------
def obj_dir(obj, t0, t1, dt, x0, theta, model=None):
    """ Compute a unit vector of objective function sensitivities, dS/dtheta.

        Parameters
        ----------
        obj: callable
            Objective function.
        t0 : float
            Initial time of LPM solution.
        t1 : float
            Final time of LPM solution.
        dt : float
            Time step length.
        x0 : float
            Initial value of LPM solution. 
        theta: array-like
            Parameter vector at which dS/dtheta is evaluated.
        
        Returns
        -------
        s : array-like
            Unit vector of objective function derivatives.

    """
    # empty list to store components of objective function derivative 
    s = np.zeros(len(theta))
    
    # compute objective function at theta
    # **uncomment and complete the command below**
    s0 = obj(t0, t1, dt, x0, theta)

    # amount by which to increment parameter
    dtheta = 1.e-8
    
    # for each parameter
    for i in range(len(theta)):
        # basis vector in parameter direction 
        eps_i = np.zeros(len(theta))
        eps_i[i] = 1.
        
        # compute objective function at incremented parameter
        # **uncomment and complete the command below**
        theta[i]+=dtheta
        si = (obj(t0, t1, dt, x0, theta)-s0)/dtheta
        theta[i]-=dtheta
        # compute objective function sensitivity
        # **uncomment and complete the command below**
        s[i] = si

    # return NORMALISED sensitivity vector
    return s/norm(s)


# **this function is incomplete**
#					 ----------
def step(theta0, s, alpha):
    """ Compute parameter update by taking step in steepest descent direction.

        Parameters
        ----------
        theta0 : array-like
            Current parameter vector.
        s : array-like
            Step direction.
        alpha : float
            Step size.
        
        Returns
        -------
        theta1 : array-like
            Updated parameter vector.
    """
    # compute new parameter vector as sum of old vector and steepest descent step
    # **uncomment and complete the command below**
    theta1 = theta0-alpha*s
    
    return theta1


# this function is NOT complete AT ALL
def line_search(obj, t0, t1, dt, x0,  theta, s):
    """ Compute step length that minimizes objective function along the search direction.

        Parameters
        ----------
        obj : callable
            Objective function.
        t0 : float
            Initial time of LPM solution.
        t1 : float
            Final time of LPM solution.
        dt : float
            Time step length.
        x0 : float
            Initial value of LPM solution.
        theta : array-like
            Parameter vector at start of line search.
        s : array-like
            Search direction (objective function sensitivity vector).
    
        Returns
        -------
        alpha : float
            Step length.
    """
    # initial step size
    alpha = 0.
    # objective function at start of line search
    s0 = obj(t0, t1, dt, x0, theta)
    # anonymous function: evaluate objective function along line, parameter is a
    sa = lambda a: obj(t0, t1, dt, x0, theta-a*s)
    # compute initial Jacobian: is objective function increasing along search direction?
    j = (sa(.01)-s0)/0.01
    # iteration control
    N_max = 500
    N_it = 0
    # begin search
        # exit when (i) Jacobian very small (optimium step size found), or (ii) max iterations exceeded
    while abs(j) > 1.e-5 and N_it<N_max:
        # increment step size by Jacobian
        alpha += -j
        # compute new objective function
        si = sa(alpha)
        # compute new Jacobian
        j = (sa(alpha+0.01)-si)/0.01
        # increment
        N_it += 1
    # return step size
    return alpha



from lpm_solving_functions import *
from ode_functions import *
from data_prep_functions import load_pressures,load_concs

# this function is incomplete
def pressure_obj(t0, t1, dt, x0, theta, model=None):
    """ Evaluate pressure LPM at theta.

        Parameters
        ----------
        t0 : float
            Initial time of solution.
        t1 : float
            Final time of solution.
        dt : float
            Time step length.
        x0 : float
            Initial value of solution.        
        theta : array-like 
            [a, b, p0, p1] parameter space for pressure ode
        model : callable
            This input always ignored, but required for consistency with obj_dir.
        
        Returns
        -------
        s : float
            Value of objective function at theta.
    """

    #solve the model with theta's parameters
    t, p=solve_ode_pressure(pressure_ode, t0, t1, dt, x0, theta)

    #get the measured pressures
    times, pressures=load_pressures()

    r=np.zeros(len(times))
    #Calculate the residuals for each data point
    for i in range(len(t)):
        #look through both time arrays to find similar times
        for j in range(len(times)):
            if abs(times[j]-t[i])<1.e-6: #if the times are the same
                #take the absolute difference for the data point
                r[j]=abs(p[i]-pressures[j])
    

    #return the sum of residuals
    return  sum(r)

def conc_obj(t0, t1, dt, x0, pv, tv, theta, model=None):
    """ Evaluate conc LPM at theta.

        Parameters
        ----------
        t0 : float
            Initial time of solution.
        t1 : float
            Final time of solution.
        dt : float
            Time step length.
        x0 : float
            Initial value of solution.        
        pv : array-like
            Solution to the pressure LPM - a linking variable
        tv : array-like
            Times the pressure LPM has pressures for
        theta : array-like 
            [d, m0, csrc] parameter space for conc ode
        model : callable
            This input always ignored, but required for consistency with obj_dir.
        
        Returns
        -------
        s : float
            Value of objective function at theta.
    """

    #solve the model with theta's parameters
    t, c=solve_ode_conc(conc_ode, t0, t1, dt, x0, pv, tv, theta)

    #get the measured pressures
    times, concs=load_concs()

    r=np.zeros(len(times))
    #Calculate the residuals for each data point
    for i in range(len(t)):
        #look through both time arrays to find similar times
        for j in range(len(times)):
            if abs(times[j]-t[i])<1.e-6: #if the times are the same
                #take the absolute difference for the data point
                r[j]=abs(c[i]-concs[j])
    

    #return the sum of residuals
    return  sum(r)


def conc_obj_dir(obj, t0, t1, dt, x0, pv, tv, theta, model=None):
    """ Compute a unit vector of objective function sensitivities, dS/dtheta.

        Parameters
        ----------
        obj: callable
            Objective function.
        t0 : float
            Initial time of LPM solution.
        t1 : float
            Final time of LPM solution.
        dt : float
            Time step length.
        x0 : float
            Initial value of LPM solution.
        pv : array-like
            Solution to the pressure LPM - a linking variable
        tv : array-like
            Times the pressure LPM has pressures for 
        theta: array-like
            Parameter vector at which dS/dtheta is evaluated.
        
        Returns
        -------
        s : array-like
            Unit vector of objective function derivatives.
        
        Notes
        -----
        This function should only be used in calibrating the conc LPM
    """
    # empty list to store components of objective function derivative 
    s = np.zeros(len(theta))
    
    # compute objective function at theta
    # **uncomment and complete the command below**
    s0 = conc_obj(t0, t1, dt, x0, pv, tv, theta)

    # for the final three conc parameters
    for i in [4,5,6]:
    #for i in range(len(theta[4:-1])):
        # basis vector in parameter direction 
        eps_i = np.zeros(len(theta))
        eps_i[i] = 1.
        
        # amount by which to increment parameter
        #calibration of conc lpm is hard since the respective magnitudes vary hugely:
        if i!=6:#first two params to calibrate are on order of 10^8 and 10^10
            dtheta=10
        else:#final param is on the order of 10^-6
            dtheta=1.e-8
        # compute objective function at incremented parameter
        # **uncomment and complete the command below**
        theta[i]+=dtheta
        si = (conc_obj(t0, t1, dt, x0, pv, tv, theta)-s0)/dtheta
        theta[i]-=dtheta
        # compute objective function sensitivity
        # **uncomment and complete the command below**
        s[i] = si

    # return NORMALISED sensitivity vector
    return s/norm(s)