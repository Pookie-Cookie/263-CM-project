import lpm_solve as ls
import numpy as np
from scipy import integrate
from matplotlib import pyplot as plt
import data_prep_functions as dpf


def plot_pressure_benchmark(save):
    ''' Plots the benchmark of the pressure lpm against an analytical solution

        Parameters:
        ----------
        save : Bool
			If set to true, save BOTH figures generated to working directory

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

    #obtain numerical solution with same parameter values
    numerical = ls.solve_p_lpm(t, 1, 3, 4, 5, testing = [True, t, [1], np.full(n, 2)])

    #plot
    f, ax = plt.subplots(1, 1)
    ax.plot(t, numerical, 'k-o', label='Numerical')
    ax.plot(t, analytical, 'b', label='Analytical')
    ax.legend(prop={'size':14})
    ax.set_title('a = 1, b = 3, $P_0$ = 4, $P_1$ = 5, $P(0)$ = 1, and $q$ = 2 [held constant]')
    f.suptitle("Comparison of analytical and numerical solutions to pressure LPM")
    
    save_figure = save
    if not save_figure:
        #Open a new window and display the plot
        plt.show()
    else:
        #Save that plot to a png file
        plt.savefig('pressure_benchmark.png',dpi=300)




def plot_conc_benchmark(save):
    ''' Plots the benchmark of the concentration lpm against an analytical solution

        Parameters:
        ----------
		save : Bool
			If set to true, save figure generated to working directory

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

    #plot
    f, ax = plt.subplots(1, 1)
    ax.plot(t, numerical, 'k-o', label='Numerical')
    ax.plot(t, analytical, 'b', label='Analytical')
    ax.legend(loc='lower left', prop={'size':14})
    ax.set_title('a = 1, b = 3, $P_0$ = 4, $P_1$ = 5, d = 7, $M_0$=3, $C_{src}$ = 1, C(0)=1, and $P$ = 6 [held constant]',size=10)
    f.suptitle("Comparison of analytical and numerical solutions to concentration LPM")
    
    save_figure = save
    if not save_figure:
        #Open a new window and display the plot
        plt.show()
    else:
        #Save that plot to a png file
        plt.savefig('conc_benchmark.png',dpi=300)

    


    


'''
if __name__ == "__main__":
    #plot_pressure_benchmark()
    plot_conc_benchmark()
'''