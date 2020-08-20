#Contains a solution for the pressure LPM for Onehunga Aquifer formulation.

#from ode_functions import *
#from lpm_solving_functions import solve_ode_pressure
from data_prep_functions import load_pressures
from matplotlib import pyplot as plt
from ode_functions import pressure_ode
from lpm_solving_functions import solve_ode_pressure

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
    
    #plot model values
    #t,Tmod=solve_ode_kettle(ode_model,0,1260,0.1,21,[0.0004545,0.00039,21])
    
    #p_initial=pressure_unit_convert(3.13*10**(-2))
    
    #AD-HOC PARAMETER TESTING
    #t, p=solve_ode_pressure(pressure_ode,1980,2016,1,0.0313,[0.00055,0.15984,-0.04974,0.060258])
    #t, p=solve_ode_pressure(pressure_ode,1980,2016,1,0.0313,[0.00045,0.115,-0.01,0.045258])
    t, p=solve_ode_pressure(pressure_ode,1980,2016,1,0.0313,[0.000472429035, 0.159837519513, -0.049742594109, 0.060255405891])

    #t, p=solve_ode_pressure(pressure_ode,1980,2016,1,0.0313,[0.0001,0.0001,-0.05,0.05])
    #t,p=solve_ode_pressure(pressure_ode,1980,2016,0.1,p_initial,[a,b,p0,p1])
    
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