import lpm_solve as ls
import numpy as np
from scipy import integrate
from matplotlib import pyplot as plt
import data_prep_functions as dpf


def plot_pressure_benchmark():
    #analytical solution obtained via wolfram, parameters are as follows:
    #a = 1, q = 2, b = 3, P0 = 4, P1 = 5 and P(0) = 1
    t = np.arange(1980, 2015, 1)
    analytical = 29/6-(23e-6*t)/6

    def solve_p_lpm(t,a,b,p0,p1):
        # load pressure data - to get the initial value
        tp,p = dpf.load_pressures()
        print(tp)
        tp = t
        # initial value
        p[0] = 1
        pm = [p[0],]                            
        # solve at pressure steps
        for t0,t1 in zip(tp[:-1],tp[1:]):          
            # predictor gradient
            dpdt1 = ls.p_lpm(pm[-1]-p[0], t0, a, b, p0, p1)
            # predictor step
            pp = pm[-1] + dpdt1*(t1-t0)
            # corrector gradient             
            dpdt2 = ls.p_lpm(pp-p[0], t1, a, b, p0, p1)
            # corrector step       
            pm.append(pm[-1] + 0.5*(t1-t0)*(dpdt2+dpdt1))

        # interp onto requested times  
        return np.interp(t, tp, pm)

    numerical = solve_p_lpm(t, 1, 3, 4, 5)

    f, ax = plt.subplots(1, 1)
    ax.plot(t, numerical, 'k')
    ax.plot(t, analytical, 'b')
    plt.show()




'''def plot_conc_benchmark():
    y = integrate.odeint(ls.c_lpm(1, 1, 1, 1, 1, 1, 1, 1, 1), 1, np.arange(1980, 2020, 1))
    y_numerical = ls.solve_c_lpm(np.arange(1980, 2020, 1), 1, 1, 1, 1, 1, 1, 1)
    return '''




plot_pressure_benchmark()