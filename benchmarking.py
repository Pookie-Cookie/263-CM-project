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

    numerical = ls.solve_p_lpm(t, 1, 3, 4, 3, testing = [True, t, [1], np.full(n, 2)])

    f, ax = plt.subplots(1, 1)
    ax.plot(t, numerical, 'k--')
    ax.plot(t, analytical, 'b')
    plt.show()




'''def plot_conc_benchmark():
    y = integrate.odeint(ls.c_lpm(1, 1, 1, 1, 1, 1, 1, 1, 1), 1, np.arange(1980, 2020, 1))
    y_numerical = ls.solve_c_lpm(np.arange(1980, 2020, 1), 1, 1, 1, 1, 1, 1, 1)
    return '''




plot_pressure_benchmark()