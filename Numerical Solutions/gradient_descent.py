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


# **this function is incomplete**
#					 ----------
def obj_dir(obj, theta, model=None):
    """ Compute a unit vector of objective function sensitivities, dS/dtheta.

        Parameters
        ----------
        obj: callable
            Objective function.
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
    s0 = obj(theta)

    # amount by which to increment parameter
    dtheta = 1.e-2
    
    # for each parameter
    for i in range(len(theta)):
        # basis vector in parameter direction 
        eps_i = np.zeros(len(theta))
        eps_i[i] = 1.
        
        # compute objective function at incremented parameter
        # **uncomment and complete the command below**
        theta[i]+=dtheta
        si = (obj(theta)-s0)/dtheta
        theta[i]-=dtheta
        # compute objective function sensitivity
        # **uncomment and complete the command below**
        s[i] = si

    # return sensitivity vector
    return s


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


# this function is complete
def line_search(obj, theta, s):
    """ Compute step length that minimizes objective function along the search direction.

        Parameters
        ----------
        obj : callable
            Objective function.
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
    s0 = obj(theta)
    # anonymous function: evaluate objective function along line, parameter is a
    sa = lambda a: obj(theta-a*s)
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



from lpm_solving_functions import solve_ode_pressure
from ode_functions import pressure_ode
from data_prep_functions import load_pressures

# this function is incomplete
def pressure_obj(theta, model=None):
    """ Evaluate pressure LPM at theta.

        Parameters
        ----------
        theta : array-like 
            [a, b, p0, p1] paramter space for pressure ode
        model : callable
            This input always ignored, but required for consistency with obj_dir.
        
        Returns
        -------
        s : float
            Value of objective function at theta.
    """

    #solve the model with theta's parameters
    t, p=solve_ode_pressure(pressure_ode,1980,2016,1,0.0313,theta)

    #get the measured pressures
    times, pressures=load_pressures()

    r=np.zeros(len(times))
    #Calculate the residuals for each data point
    for i in range(len(t)):
        #look through both time arrays to find similar times
        for j in range(len(times)):
            if abs(times[j]-t[i])<1.e-6: #if the times are the same
                #take the difference squared for the data point
                r[j]=(p[i]-pressures[j])**2
    

    #return the sum of residuals
    return  sum(r)

    