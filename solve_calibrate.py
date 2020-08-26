from data_prep_functions import *
from lpm_solve import *
from matplotlib import pyplot as plt

def pressure_lpm_model():
    ''' Solves the pressure LPM and displays solution before saving it to a csv file.

        Parameters
        ----------
        None

        Returns
        -------
        pm : array-like
            Vector containing solutions to pressure LPM at times tp
        tp : array-like
            Vector containing times for which pressure LPM is solved
        pars : array-like
            Vector containing parameters a,b,p0,p1 for which the LPM best fits the data

        Notes
        -----
        Saves a csv file containing the solution and solution times to the working directory.
        Must be called before attempting to run conc_lpm_model.
    '''
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
    f.suptitle("Comparison between pressure LPM and data for the Onehunga Aquifer",size=15)
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

    misfit = pm-p
    f, ax = plt.subplots(1, 1)
    ax.plot(tp, misfit, 'ko', label='misfit(Mpa)')
    ax.plot(tp, np.zeros(np.size(tp)), 'k--', label='baseline 0')
    ax.set_title('pressure misfit plot')
    ax.set_ylabel('pressure misfit [Mpa]')
    ax.set_xlabel('time[year]')
    plt.show()

    return pm, tp, pars

def conc_lpm_model(pm,tp,pressure_pars):
    ''' Solves the conc LPM and displays solution.

        Parameters
        ----------
        pm : array-like
            Vector containing solutions to pressure LPM at times tp
        tp : array-like
            Vector containing times for which pressure LPM is solved
        pressure_pars : array-like
            Vector containing parameters a,b,p0,p1 for which pressure LPM best fits pressure data 

        Returns
        -------
        None

        Notes
        -----
        Saves a csv file containing the solution and solution times to the working directory.
        Must call pressure_lpm_model before attempting to run.
        Only parameters d, m0, csrc are calibrated in this function 
        - the rest are obtained from calibrating the pressure LPM.
    '''
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
    f.suptitle("Comparison between copper concentration LPM and data for the Onehunga Aquifer",size=15)
    plt.show()

if __name__ == "__main__":
    pm, tm, pars = pressure_lpm_model()
    conc_lpm_model(pm,tm,pars)

    