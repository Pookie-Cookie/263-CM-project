import lpm_solve as ls
import numpy as np
from scipy import integrate
from matplotlib import pyplot as plt
import data_prep_functions as dpf


def plot_pressure_benchmark():
    #analytical solution obtained via wolfram, parameters are as follows:
    #a = 1, q = 2, b = 3, P0 = 4, P1 = 5 and P(0) = 1
    n=100
    t = np.linspace(0, 5, num=n)
    analytical = 25/6-19*(np.exp(-6*t))/6

    numerical = ls.solve_p_lpm(t, 1, 3, 4, 5, testing = [True, t, [1], np.full(n, 2)])

    f, ax = plt.subplots(1, 1)
    ax.plot(t, numerical, 'k--')
    ax.plot(t, analytical, 'b')
    plt.show()




def plot_conc_benchmark():
    #analytical solution obtained via wolfram, parameters are as follows:
    #a = 1, b = 3, P0 = 4, P1 = 5, P = 6, d = 7, Csrc = 1, C(0)=1, M0=3
    n=100
    t = np.linspace(0, 5, num=n)
    analytical = 3.5-2.5*np.exp(t)

    numerical = ls.solve_c_lpm(t, 1, 3, 4, 5, 7, 3, 1, testing = [True, t, [1], np.full(n, 6)])

    f, ax = plt.subplots(1, 1)
    ax.plot(t, numerical, 'k--')
    ax.plot(t, analytical, 'b')
    plt.show()
    


    



if __name__ == "__main__":
    #plot_pressure_benchmark()
    plot_conc_benchmark()
