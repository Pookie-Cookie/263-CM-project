#Contains a solution for the pressure LPM for Onehunga Aquifer formulation.

#from ode_functions import *
#from lpm_solving_functions import solve_ode_pressure
import numpy as np
from data_prep_functions import load_pressures
from matplotlib import pyplot as plt
from ode_functions import pressure_ode
from lpm_solving_functions import solve_ode_pressure
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
        none

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
        plt.savefig('model_vs_expt.png',dpi=300)


if __name__ == "__main__":
    plot_pressure_model()

    print("Finished")