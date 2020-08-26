#Contains a solution for the pressure LPM for Onehunga Aquifer formulation.

#from ode_functions import *
#from lpm_solving_functions import solve_ode_pressure
import numpy as np
from data_prep_functions import load_pressures,load_concs,conc_unit_convert
from matplotlib import pyplot as plt
from ode_functions import *
from lpm_solving_functions import *
from calibration import *

#############################################################################################
#PLOTTING FUNCTIONS
#############################################################################################

def plot_pressure_model():
    ''' Plot the pressure LPM over top of the data.

        Parameters:
        -----------
        none

        Returns:
        --------
        t : array-like
            Times the pressure LPM has pressures for
        p : array-like
            Solution to the pressure LPM - a linking variable
        theta_better : array-like
            Set of parameters where pressure objective function is lowest(of the start points tested in calibration)

        Notes:
        ------
        This function called within if __name__ == "__main__":

        It should contain commands to read and plot the experimental data, run and 
        plot the pressure LPM for hard coded parameters, and then either display the 
        plot to the screen or save it to the disk.

    '''
    #get experimental data
    t,P=load_pressures()

    f,ax=plt.subplots(1,1)
    #plot measured values
    
    ax.plot(t,P,'ro', label='Measured')
    
    #Values needed to solve and calibrate DE 
    t0=1980 #taken from data
    t1=2016 #taken from data
    dt=1
    p_start=0.0313 #taken from data
    
    #CALIBRATE using gradient descent
    n=20 #test a reasonable no. of starting points but not too many - otherwise too slow
    theta_better, s_better=rand_pressure_params(n, t0, t1, dt, p_start)


    #SOLVE using parameters from gradient descent
    t, p=solve_ode_pressure(pressure_ode, t0, t1, dt, p_start, theta_better)

    #plot model solution
    ax.plot(t,p,'b-',label='Model')

    #set titles of graph and axes
    ax.set_xlabel('time[s]')
    ax.set_ylabel('pressure[MPa]')
    ax.set_title("Pressure LPM calibrated using gradient descent iterating over {:d} randomly-generated start parameters $\\theta$".format(n), size=7)
    ax.text(2005,-0.005,'LPM solution has\n the following parameters:\n $a=${:6f},\n $b=${:6f},\n $P_0$={:6f} MPa,\n $P_1$={:6f}MPa'.format(theta_better[0], theta_better[1], theta_better[2], theta_better[3]),size=7)

    f.suptitle("Variation in pressure of Onehunga Aquifer")
    f.legend(loc="upper right",bbox_to_anchor=(1,1),bbox_transform=ax.transAxes)

    save_figure = False
    if not save_figure:
        #Open a new window and display the plot
        plt.show()
    else:
        #Save that plot to a png file
        plt.savefig('pressure_model_vs_data.png',dpi=300)
    
    return t, p, theta_better



def plot_conc_model(tv, pv, theta_better):
    ''' Plot the conc LPM over top of the data.

        Parameters:
        -----------
        pv : array-like
            Solution to the pressure LPM - a linking variable
        tv : array-like
            Times the pressure LPM has pressures for
        theta_better : array-like
            Vector of parameters which pressure model has been calibrated to

        Returns:
        --------
        none

        Notes:
        ------
        theta_better contains, in the following order, parameters:
        a,b,p0,p1
        
        This function called within if __name__ == "__main__":

        It should contain commands to read and plot the experimental data, run and 
        plot the concentration LPM for hard coded parameters, and then either display the 
        plot to the screen or save it to the disk.
    '''    
    #get experimental data
    t,C=load_concs()

    #convert to mass fraction
    C=conc_unit_convert(C)

    f,ax=plt.subplots(1,1, figsize=(9,7))
    #plot measured values
    
    ax.plot(t,C,'ro', label='Measured')

    #get parameters for pressure LPM:
    a=theta_better[0]
    b=theta_better[1]
    p0=theta_better[2]
    p1=theta_better[3]
    
    #Values needed to solve and calibrate DE 
    t0=1980 #taken from data
    t1=2015 #taken from data
    dt=1
    c_start=0.0 #taken from data

    #AD-HOC calibration of d, m0, csrc
    d=50.e8
    m0=1.e10
    csrc=2.e-6
    
    #since a,b,p0,p1 are known, only need to calibrate 3 variables
    theta=np.array([a, b, p0, p1, d, m0, csrc])
    theta_best=conc_params(t0, t1, dt, c_start, pv, tv, theta)
    
    #CALIBRATE using gradient descent
    n=20 #test a reasonable no. of starting points but not too many - otherwise too slow
    theta_best, s_best = rand_pressure_params(n, t0, t1, dt, x0, pv, tv, theta_better)
    #SOLVE using parameters from gradient descent
    t, c=solve_ode_conc(conc_ode, t0, t1, dt, c_start, pv, tv, theta_best[0])

    #plot model solution
    ax.plot(t,c,'b-',label='Model')

    #set titles of graph and axes
    ax.set_xlabel('time[s]')
    ax.set_ylabel('concentration[mass fraction]')
    #ax.set_title("Pressure LPM calibrated using gradient descent iterating over {:d} randomly-generated start parameters $\\theta$".format(n), size=7)
    #ax.text(2005,-0.005,'LPM solution has\n the following parameters:\n $a=${:6f},\n $b=${:6f},\n $P_0$={:6f} MPa,\n $P_1$={:6f}MPa'.format(theta_better[0], theta_better[1], theta_better[2], theta_better[3]),size=7)

    f.suptitle("Variation in copper concentration of Onehunga Aquifer")
    f.legend(loc="upper right",bbox_to_anchor=(1,1),bbox_transform=ax.transAxes)


    save_figure = False
    if not save_figure:
        #Open a new window and display the plot
        plt.show()
    else:
        #Save that plot to a png file
        plt.savefig('conc_model_vs_data.png',dpi=300)

if __name__ == "__main__":
    #tv, pv, theta_better=plot_pressure_model()
    pv=np.array([ 0.0313    ,  0.02138905,  0.01253653,  0.00458992, -0.00250368,
       -0.00846848, -0.01404959, -0.01899304, -0.02366041, -0.02792519,
       -0.0315559 , -0.03465197, -0.03721989, -0.03930559, -0.04111028,
       -0.04264899, -0.04290819, -0.04369863, -0.04473243, -0.04591876,
       -0.04713788, -0.04460112, -0.04246216, -0.04069139, -0.03910183,
       -0.03779161, -0.03650435, -0.0353177 , -0.03438013, -0.03357995,
       -0.03289998, -0.03222454, -0.0317745 , -0.0311593 , -0.03066131,
       -0.03034639, -0.02984943])
    tv=np.array([1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990,
       1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001,
       2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012,
       2013, 2014, 2015, 2016])
    theta_better=np.array([ 0.07875637,  0.06703037, -0.00142697,  0.00694487])

    plot_conc_model(tv, pv, theta_better)

    print("Finished")