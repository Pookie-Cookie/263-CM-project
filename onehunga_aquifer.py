#Contains a solution for the pressure LPM for Onehunga Aquifer formulation.

#from ode_functions import *
#from lpm_solving_functions import solve_ode_pressure
import numpy as np
from data_prep_functions import load_pressures
from matplotlib import pyplot as plt
from ode_functions import pressure_ode
from lpm_solving_functions import solve_ode_pressure
from calibration import pressure_params

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
    t0=1980
    t1=2016
    dt=1
    p_start=0.0313
    
    theta0=np.array([0.00055,0.00055,-0.05,0.08])
    #CALIBRATE using gradient descent
    #good_theta=pressure_params(t0, t1, dt, p_start, theta0)
    #t, p=solve_ode_pressure(pressure_ode, t0, t1, dt, p_start, good_theta)
    #t, p=solve_ode_pressure(pressure_ode, t0, t1, dt, p_start, np.array([0.05515084, 0.02670687, 0.01719836, -0.02844045]))
    t, p=solve_ode_pressure(pressure_ode, t0, t1, dt, p_start, np.array([0.08493392, 0.04646894, 0.02130564, 0.02323962]))

    ax.plot(t,p,'b-',label='Model')

    #set titles of graph and axes
    ax.set_xlabel('time[s]')
    ax.set_ylabel('pressure[MPa]')
    ax.set_title("Variation in pressure of Onehunga Aquifer")
    ax.text(600,20,'Pressure in 1980 - $3.13\times 10^{-2}$ MPa',size=7)

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