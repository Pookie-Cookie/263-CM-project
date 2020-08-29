import lpm_solve as ls
import numpy as np
from scipy import integrate
from matplotlib import pyplot as plt
import data_prep_functions as dpf


def plot_pressure_benchmark():
    ''' Plots the benchmark of the pressure lpm against an analytical solution

        Parameters:
        ----------
        None

        Returns:
        --------
        None

        Notes:
        This will output a plot to the screen where a plot of the numerical and analytical solution is overlayed on top
        dotted broken line is numerical and solid blue line is analytical.

    '''
    #analytical solution obtained via wolfram, parameters are as follows:
    #a = 1, q = 2, b = 3, P0 = 4, P1 = 5 and P(0) = 1
    n=100
    t = np.linspace(0, 5, num=n)
    analytical = 25/6-19*(np.exp(-6*t))/6

    numerical = ls.solve_p_lpm(t, 1, 3, 4, 5, testing = [True, t, [1], np.full(n, 2)])

    f, ax = plt.subplots(1, 1)
    ax.plot(t, numerical, 'k--')
    ax.plot(t, analytical, 'b')
    ax.set_title('pressure analytical vs numerical')
    
    save_figure = False
    if not save_figure:
        #Open a new window and display the plot
        plt.show()
    else:
        #Save that plot to a png file
        plt.savefig('pressure analytical vs numerical',dpi=300)




def plot_conc_benchmark():
    ''' Plots the benchmark of the concentration lpm against an analytical solution

        Parameters:
        ----------
        None

        Returns:
        --------
        None

        Notes:
        This will output a plot to the screen where a plot of the numerical and analytical solution is overlayed on top
        dotted broken line is numerical and solid blue line is analytical.

    '''
    #analytical solution obtained via wolfram, parameters are as follows:
    #a = 1, b = 3, P0 = 4, P1 = 5, P = 6, d = 7, Csrc = 1, C(0)=1, M0=3
    n=100
    t = np.linspace(0, 5, num=n)
    analytical = 3.5-2.5*np.exp(t)

    #obtain numerical solution for conc lpm
    numerical = ls.solve_c_lpm(t, 1, 3, 4, 5, 7, 3, 1, testing = [True, t, [1], np.full(n, 6)])

    f, ax = plt.subplots(1, 1)
    ax.plot(t, numerical, 'k--')
    ax.plot(t, analytical, 'b') 
    ax.set_title('concentration analytical vs numerical')

    save_figure = False
    if not save_figure:
        #Open a new window and display the plot
        plt.show()
    else:
        #Save that plot to a png file
        plt.savefig('concentration analytical vs numerical',dpi=300)
   
    


    



if __name__ == "__main__":
    #plot_pressure_benchmark()
    plot_conc_benchmark()
