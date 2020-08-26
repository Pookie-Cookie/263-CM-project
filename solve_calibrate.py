from data_prep_functions import *
from lpm_solve import *
from matplotlib import pyplot as plt

def pressure_lpm_model():
    # load pressure data
    tp,p = load_pressures()
        
    # use CURVE_FIT to find "best" model
    from scipy.optimize import curve_fit
    pars = curve_fit(solve_p_lpm, tp, p, [0.005,0.005,-0.005,0.005])[0]

    # plot the best solution
    pm = solve_p_lpm(tp,*pars)
    f,ax = plt.subplots(1,1,figsize=(12,8))
    ax.plot(tp, p, 'ro', label = 'observations')
    ax.plot(tp, pm, 'k-', label='model')
    ax.set_ylabel("pressure [MPa]",size=14); ax.set_xlabel("time[year]",size=14)
    ax.legend(prop={'size':14})
    ax.set_title('a={:2.1e},   b={:2.1e},   p0={:2.1e},  p1={:2.1e}'.format(*pars),size=14)
    plt.show()

    #save the solution to a file to be read 
    #store the solution in a single array
    pressure_soln = np.column_stack((tp,pm))
    #save the pressure solution to a .txt file
    # opening a file
    fp = open('p_lpm_soln.txt','w')
    #write header
    fp.write('t[year], P[MPa]\n')
    #enter pressure solution data
    [fp.write('{:f}, {:f}\n'.format(t,p)) for t, p in pressure_soln]  

    return pm, tp, pars

def conc_lpm_model(pm,tp,pressure_pars):
    #get the calibrated pressure params
    a, b, p0, p1 = [par for par in pressure_pars]
    
    # load conc data and compute derivative
    tc,c = load_concs()
    c = conc_unit_convert(c)
        
    # use CURVE_FIT to find "best" model
    from scipy.optimize import curve_fit
    #use parameter bounds to effectively fix params a,b,p0,p1
    e=np.finfo(float).eps
    #calibrate pressure model 
    pars = curve_fit(solve_c_lpm, tc, c, [a, b, p0, p1, 0.5e9, 1.e10, 2.e-6], bounds=([a-e,b-e,p0-e,p1-e,-np.inf, -np.inf, -np.inf],[a,b,p0,p1,np.inf, np.inf, np.inf]))[0]
    pars = np.append(pressure_pars,pars[4:])
    
    # plot the best solution
    cm = solve_c_lpm(tp,*pars)
    f,ax = plt.subplots(1,1,figsize=(12,8))
    ax.plot(tc, c, 'ro', label = 'observations')
    ax.plot(tp, cm, 'k-', label='model')
    ax.set_ylabel("concentration [mass fraction]",size=14); ax.set_xlabel("time[year]",size=14)
    ax.legend(prop={'size':14})
    ax.set_title('a={:2.1e},   b={:2.1e},   p0={:2.1e},  p1={:2.1e}, d={:2.1e}, m0={:2.1e}, csrc={:2.1e}'.format(*pars),size=14)
    plt.show()

if __name__ == "__main__":
    pm, tm, pars = pressure_lpm_model()
    conc_lpm_model(pm,tm,pars)

    