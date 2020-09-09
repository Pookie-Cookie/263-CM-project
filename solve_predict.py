from data_prep_functions import *
from lpm_solve import *
from matplotlib import pyplot as plt

def pressure_lpm_predict(level, endyear):
    ''' Solves the pressure LPM for different possible extraction rates, saving them to csv files

        Parameters
        ----------
        level : array-like
            Volume rates of extraction to predict for
        
        endyear : int
            The year up to which extrapolations should be made

        Returns
        -------
        pm : array-like
            Vector containing solutions to pressure LPM at times tp under different extractions
        tp : array-like
            Vector containing times for which pressure LPM is solved under different extractions
        pars : array-like
            Vector containing parameters a,b,p0,p1 for which the LPM best fits the data

        Notes
        -----
        Must be called before attempting to run conc_lpm_predict.
    '''
    # load pressure data
    tp,p = load_pressures()
    
    # use CURVE_FIT to find "best" model
    from scipy.optimize import curve_fit
    pars = curve_fit(solve_p_lpm, tp, p, [0.005,0.005,-0.005,0.005])[0]

    pm=[]
    tq=[]
    for i in range(len(level)):
        # change the pressure data to contain future levels of extraction
        tqi, q = future_extraction_rates(level[i], endyear)
            
        # get the best solution
        pmi = solve_p_lpm(tqi,*pars, extrapolate=tqi)
        
        #save the solution to a file to be read 
        #store the solution in a single array
        pressure_soln = np.column_stack((tqi,pmi))
        #save the pressure solution to a .txt file
        # opening a file
        fp = open('p_soln_q_{:d}.txt'.format(level[i]),'w')
        #write header
        fp.write('t[year], P[MPa]\n')
        #enter pressure solution data
        [fp.write('{:f}, {:f}\n'.format(t,p)) for t, p in pressure_soln]
        fp.close()
        pm.append(pmi)
        tq.append(tqi)
          


    return pm, tq, pars

def conc_lpm_predict(pm,tp,pressure_pars,levels,save):
    ''' Solves the conc LPM under various extractions and displays solution.

        Parameters
        ----------
        pm : array-like
            Vector containing solutions to pressure LPM at times tp
        tp : array-like
            Vector containing times for which pressure LPM is solved
        pressure_pars : array-like
            Vector containing parameters a,b,p0,p1 for which pressure LPM best fits pressure data
        levels : array-like
            the level of future extraction being modelled.
		save : Bool
			If set to true, save figure generated to working directory   

        Returns
        -------
        None

        Notes
        -----
        Saves a csv file containing the solution and solution times to the working directory.
        MUST CALL pressure_lpm_model() in solve_calibrate.py BEFORE attempting to RUN.
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
    
    
    cm=[]
    for i in range(len(tp)):
        # get and store the best solutions
        cmi = solve_c_lpm(tp[i],*pars, extrapolate=tp[i], level=levels[i])
        cm.append(cmi)

    
    f,ax = plt.subplots(1,1,figsize=(12,8))
    ax.plot(tc, c/1.e-6, 'ro', label = 'observations')

    for i in range(len(levels)):
        ax.plot(tp[i], cm[i]/1.e-6, label='q={:3.1f} megalitres/day'.format(levels[i]))
    
    #solve for the historical data as well
    ch = solve_c_lpm(np.linspace(1980,2015,100), *pars, extrapolate=np.linspace(1980,2016,100), level=0)
    ax.plot(np.linspace(1980,2015,100), ch/1.e-6, 'k-', label='best-fit model')

    #plot maximum safety limit 1.76mg/L (no safety factor)
    ax.axhline(1.76, color='y', linestyle='--', label='Maximum potable copper conc')

    ax.set_ylabel("concentration [mg/L]",size=14); ax.set_xlabel("time[year]",size=14)
    ax.legend(prop={'size':11})
    ax.set_title('d={:2.1e}, $M_0$={:2.1e} kg, $Csrc$={:2.1e} mg/L'.format(*pars[4:]),size=14)
    ax.text(2030,0.0000000,'Model also uses constants\n from calibrated pressure LPM:\n $a=${:3.3f},\n $b=${:3.3f},\n $P_0$={:3.3f} MPa,\n $P_1$={:3.3f}MPa'.format(*pars[0:4]),size=12)
    f.suptitle("Solutions to copper concentration LPM for various extraction levels",size=15)
    
    save_figure = save
    if not save_figure:
        #Open a new window and display the plot
        plt.show()
    else:
        #Save that plot to a png file
        plt.savefig('conc_predictions.png',dpi=300)


def conc_lpm_uncertain(pm,tp,pressure_pars,levels,save):
    ''' Solves the conc LPM for uncertainty in the data and displays solution.

        Parameters
        ----------
        pm : array-like
            Vector containing solutions to pressure LPM at times tp
        tp : array-like
            Vector containing times for which pressure LPM is solved
        pressure_pars : array-like
            Vector containing parameters a,b,p0,p1 for which pressure LPM best fits pressure data
        levels : array-like
            the level of future extraction being modelled.
		save : Bool
			If set to true, save figure generated to working directory   

        Returns
        -------
        None

        Notes
        -----
        Saves a csv file containing the solution and solution times to the working directory.
        MUST CALL pressure_lpm_model() in solve_calibrate.py BEFORE attempting to RUN.
        Only parameters d, m0, csrc are calibrated in this function 
        - the rest are obtained from calibrating the pressure LPM.
    '''
    #get the calibrated pressure params
    a, b, p0, p1 = [par for par in pressure_pars]
    
    # load conc data and compute derivative
    tc,c = load_concs()
    c = conc_unit_convert(c)
    
    #set error
    v=0.24e-7
    # get deviation vector
    sigma = [v]*len(tc)

            
    # use CURVE_FIT to find "best" model
    from scipy.optimize import curve_fit
    #use parameter bounds to effectively fix params a,b,p0,p1
    e=np.finfo(float).eps
    #calibrate conc model 
    #pars, cov = curve_fit(solve_c_lpm, tc, c, [a, b, p0, p1, 0.5e9, 1.e10, 2.e-6], bounds=([a-e,b-e,p0-e,p1-e,-np.inf, -np.inf, -np.inf],[a,b,p0,p1,np.inf, np.inf, np.inf]), sigma=sigma)
    #pars = np.append(pressure_pars,pars[4:])
    pars, cov = curve_fit(solve_c_lpm, tc, c, [a, b, p0, p1, 0.5e9, 1.e10, 2.e-6], sigma=sigma, absolute_sigma=True, method='dogbox')
    #pars = np.append(pressure_pars,pars[4:])
    
    cm=[]
    # find solutions for each level
    for i in range(len(tp)):
        c_level=[]
        pars_s = np.random.multivariate_normal(pars, cov, 30)   # samples from posterior
        # find solutions within each level
        #for j in range(len(tp[0])):
            # get and store the best solutions
            #cmi = solve_c_lpm(tp[i][j],*pars, extrapolate=tp[i][j], level=levels[i])
        for parss in pars_s:
            cmi = solve_c_lpm(tp[i],*parss, solution = [tp[i], pm[i]])
            c_level.append(cmi)
        
        cm.append(c_level)

    
    f,ax = plt.subplots(1,1,figsize=(12,8))
    # plot data with error
    ax.plot(tc, c/1.e-6, 'ro', label = 'observations', markersize=3)
    for tci,ci in zip(tc,c/1.e-6):
        ax.plot([tci,tci],[ci-v/1.e-6,ci+v/1.e-6], 'r-', lw=0.5)
    
    colours=['C0', 'C1', 'C2', 'C3']
    i=0
    for i in range(len(tp)):
    # colour each set of possible extractions different colours
        colour=colours[i]
        # use separate command for extrap labels - to simply add them to the legend
        ax.plot([],[], '{}'.format(colour) ,label='q={:3.1f} megalitres/day'.format(levels[i]))
        

        c_level=cm[i]
        t_level=tp[i]
        for j in range(len(c_level)):
            ax.plot(t_level[:36], c_level[j][:36]/1.e-6, 'k', lw=0.5, alpha=0.4) # first 38 data values are historical data so can plot in black 
            ax.plot(t_level[35:], c_level[j][35:]/1.e-6, '{}'.format(colour), lw=0.5, alpha=0.4)


    #plot maximum safety limit 1.76mg/L (no safety factor)
    ax.axhline(1.76, color='y', linestyle='--', label='Maximum potable copper conc')

    
    ax.set_ylabel("concentration [mg/L]",size=14); ax.set_xlabel("time[year]",size=14)
    ax.legend(prop={'size':11})
    ax.set_title('Data with absolute uncertainty of {:2.1e}mg/L (found through ad-hoc methods)'.format(v/1.e-6),size=14)
    
    f.suptitle("Solutions to copper concentration LPM for various extraction levels",size=15)
    
    save_figure = save
    if not save_figure:
        #Open a new window and display the plot
        plt.show()
    else:
        #Save that plot to a png file
        plt.savefig('conc_uncertainty.png',dpi=300)



if __name__ == "__main__":
    levels=[0, 10, 20, 40]
    pm, tm, pars = pressure_lpm_predict(levels, 2050)
    conc_lpm_uncertain(pm,tm,pars,levels,save=False)

    