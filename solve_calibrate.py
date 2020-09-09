from data_prep_functions import *
from lpm_solve import *
from matplotlib import pyplot as plt

def pressure_lpm_model(save):
    ''' Solves the pressure LPM and displays solution and data misfit

        Parameters
        ----------
		save : Bool
			If set to true, save both figures generated to working directory

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
        MUST be called before attempting to run conc_lpm_model.
    '''
    # load pressure data - to calibrate parameters
    tp,p = load_pressures()
        
    # use CURVE_FIT to find "best" model
    from scipy.optimize import curve_fit
    pars = curve_fit(solve_p_lpm, tp, p, [0.005,0.005,-0.005,0.005])[0]
    # get times to evaluate soln at
    tq, q = load_extraction_rates()

    # plot the best solution
    pm = solve_p_lpm(tq,*pars, extrapolate=tq)
    f,ax = plt.subplots(1,1, constrained_layout=True)
    ax.plot(tp, p, 'ro', label = 'observations')
    ax.plot(tq, pm, 'k-', label='model')
    ax.set_ylabel("pressure [MPa]",size=14); ax.set_xlabel("time[year]",size=14)
    ax.legend(prop={'size':14})
    ax.set_title('a={:2.1e},   b={:2.1e},   P0={:2.1e},  P1={:2.1e}'.format(pars[0],pars[1],pars[2],pars[3]),size=14)
    f.suptitle("Best-fit pressure LPM",size=15)

    save_figure = save
    if not save_figure:
        #Open a new window and display the plot
        plt.show()
    else:
        #Save that plot to a png file
        plt.savefig('pressure_calibrate.png',dpi=300)

    #save the solution to a file to be read 
    #store the solution in a single array
    pressure_soln = np.column_stack((tq,pm))
    #save the pressure solution to a .txt file
    # opening a file
    fp = open('p_lpm_soln.txt','w')
    #write header
    fp.write('t[year], P[MPa]\n')
    #enter pressure solution data
    [fp.write('{:f}, {:f}\n'.format(t,p)) for t, p in pressure_soln]  
    fp.close()
    # get model values for times common to data and model
    pmis=[]
    for i in range(len(tp)):
        for j in range(len(tq)):
            if tp[i]==tq[j]:
                pmis.append(pm[j])

    misfit = pmis-p #should have length tp
    f, ax = plt.subplots(1, 1, constrained_layout=True)
    ax.plot(tp, misfit, 'ko', label='misfit(Mpa)')
    ax.plot(tp, np.zeros(np.size(tp)), 'k--', label='baseline 0')
    ax.set_title('Pressure misfit plot',size=15)
    ax.set_ylabel('pressure misfit [MPa]',size=14)
    ax.set_xlabel('time[year]',size=14)


    save_figure = save
    if not save_figure:
        #Open a new window and display the plot
        plt.show()
    else:
        #Save that plot to a png file
        plt.savefig('pressure_misfit.png',dpi=300)

    return pm, tp, pars

def conc_lpm_model(pm,tp,pressure_pars,save):
    ''' Solves the conc LPM and displays solution and misfit from data

        Parameters
        ----------
        pm : array-like
            Vector containing solutions to pressure LPM at times tp
        tp : array-like
            Vector containing times for which pressure LPM is solved
        pressure_pars : array-like
            Vector containing parameters a,b,p0,p1 for which pressure LPM best fits pressure data
		save : Bool
			If set to true, save both figures generated to working directory 

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

    # get times at which to evaluate solution
    tq, q = load_extraction_rates()
    
    # plot the best solution
    cm = solve_c_lpm(tq,*pars, extrapolate=tq)
    f,ax = plt.subplots(1,1, constrained_layout=True)
    ax.plot(tc, c, 'ro', label = 'observations')
    ax.plot(tq, cm, 'k-', label='model')
    ax.set_ylabel("concentration [mass fraction]",size=14); ax.set_xlabel("time[year]",size=14)
    ax.legend(prop={'size':14})
    ax.set_title('d={:2.1e}, $M_0$={:2.1e} kg, $Csrc$={:2.1e} mg/L'.format(*pars[4:]),size=14)
    ax.text(2000,0.0000000,'Uses constants from\n pressure LPM calibration:\n $a=${:3.3f},\n $b=${:3.3f},\n $P_0$={:3.3f} MPa,\n $P_1$={:3.3f}MPa'.format(*pars[0:4]),size=12)
    f.suptitle("Best-fit copper concentration LPM",size=15)
    #plt.tight_layout()
    save_figure = save
    if not save_figure:
        #Open a new window and display the plot
        plt.show()
    else:
        #Save that plot to a png file
        plt.savefig('conc_calibrate.png',dpi=300)


    # get model values for times common to data and model
    cmis=[]
    for i in range(len(tc)):
        for j in range(len(tq)):
            if tc[i]==tq[j]:
                cmis.append(cm[j])
    
    #misfit should only have the same not of data pts as tc
    misfit = cmis-c
    f, ax = plt.subplots(1, 1, constrained_layout=True)
    ax.plot(tc, misfit, 'ko', label='misfit[MPa]')
    ax.plot(tc, np.zeros(np.size(tc)), 'k--', label='baseline 0')
    ax.set_title('Concentration misfit',size=15)
    ax.set_ylabel('concentration misfit [Mass fraction]',size=14)
    ax.set_xlabel('time[year]', size=14)

    save_figure = save
    if not save_figure:
        #Open a new window and display the plot
        plt.show()
    else:
        #Save that plot to a png file
        plt.savefig('conc_misfit.png',dpi=300)

if __name__ == "__main__":
    pm, tm, pars = pressure_lpm_model(save=False)
    conc_lpm_model(pm,tm,pars, save=False)

    