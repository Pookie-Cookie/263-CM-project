from data_prep_functions import *
from matplotlib import pyplot as plt

def pressure_lpm_model():
    # load flow rate data and compute derivative
    tq,qi = load_extraction_rates()
    qi = extraction_unit_convert(qi)
    tp,p = load_pressures()

    # define derivative function
    def p_lpm(p,t,a,b,p0,p1):                 # order of variables important
        q = np.interp(t,tq,qi)           # interpolate (piecewise linear) flow rate
        #dqdti = np.interp(t,tq,dqdt)     # interpolate derivative
        return -a*q-b*(p-p0)-b*(p-p1)   # compute derivative

    # implement an imporved Euler step to solve the ODE
    def solve_lpm(t,a,b,p0,p1):
        pm = [p[0],]                            # initial value
        for t0,t1 in zip(tp[:-1],tp[1:]):           # solve at pressure steps
            dpdt1 = p_lpm(pm[-1]-p[0], t0, a, b, p0, p1)   # predictor gradient
            pp = pm[-1] + dpdt1*(t1-t0)             # predictor step
            dpdt2 = p_lpm(pp-p[0], t1, a, b, p0, p1)       # corrector gradient
            pm.append(pm[-1] + 0.5*(t1-t0)*(dpdt2+dpdt1))  # corrector step
        return np.interp(t, tp, pm)             # interp onto requested times
        
    # use CURVE_FIT to find "best" model
    from scipy.optimize import curve_fit
    pars = curve_fit(solve_lpm, tp, p, [0.005,0.005,-0.005,0.005])[0]

    # plot the best solution
    pm = solve_lpm(tp,*pars)
    f,ax = plt.subplots(1,1,figsize=(12,6))
    ax.plot(tp, p, 'ro', label = 'observations')
    ax.plot(tp, pm, 'k-', label='model')
    ax.set_ylabel("pressure [MPa]",size=14); ax.set_xlabel("time[year]",size=14)
    ax.legend(prop={'size':14})
    ax.set_title('a={:2.1e},   b={:2.1e},   p0={:2.1e},  p1={:2.1e}'.format(*pars),size=14)
    plt.show()

    return pm, tp, pars

def conc_lpm_model(pm,tp,pressure_pars):
    #get the calibrated pressure params
    a, b, p0, p1 = [par for par in pressure_pars]
    
    # load conc data and compute derivative
    tc,c = load_concs()
    c = conc_unit_convert(c)

    #define low pressure boundary conc
    def low_p_bound(c,p,p0):
        if p>p0:
            # contaminated water outflow happens when pressure greater inside aquifer than
            # at low pressure boundary    
            return c
        else:
            return 0

    # define derivative function
    def c_lpm(c,t,a,b,p0,p1,d,m0,csrc):                 # order of variables important
        p = np.interp(t,tp,pm)           # interpolate pressure
        #dqdti = np.interp(t,tq,dqdt)     # interpolate derivative
        cprime=low_p_bound(c,p,p0)
        #find m0*dc/dt
        mdcdt=-(b/a)*(p-p0)*(cprime-c)+(b/a)*(p-p1)*c-d*(p-((p0+p1)/2))*csrc
        #compute derivative
        return mdcdt/m0

    # implement an improved Euler step to solve the ODE
    def solve_lpm(t,a,b,p0,p1,d,m0,csrc):
        cm = [c[0],]                            # initial value
        for t0,t1 in zip(tc[:-1],tc[1:]):           # solve at conc steps
            dcdt1 = c_lpm(cm[-1]-c[0], t0, a, b, p0, p1, d, m0, csrc)   # predictor gradient
            cp = cm[-1] + dcdt1*(t1-t0)             # predictor step
            dcdt2 = c_lpm(cp-c[0], t1, a, b, p0, p1, d, m0, csrc)       # corrector gradient
            cm.append(cm[-1] + 0.5*(t1-t0)*(dcdt2+dcdt1))  # corrector step
        return np.interp(t, tc, cm)             # interp onto requested times
        
    # use CURVE_FIT to find "best" model
    from scipy.optimize import curve_fit
    pars = curve_fit(solve_lpm, tc, c, [0.005, 0.005, -0.005, 0.005, 0.5e9, 1.e10, 2.e-6])[0]

    # plot the best solution
    pm = solve_lpm(tp,*pars)
    f,ax = plt.subplots(1,1,figsize=(12,6))
    ax.plot(tc, c, 'ro', label = 'observations')
    ax.plot(tp, pm, 'k-', label='model')
    ax.set_ylabel("pressure [MPa]",size=14); ax.set_xlabel("time[year]",size=14)
    ax.legend(prop={'size':14})
    ax.set_title('a={:2.1e},   b={:2.1e},   p0={:2.1e},  p1={:2.1e}'.format(*pars),size=14)
    plt.show()

if __name__ == "__main__":
    pm, tm, pars = pressure_lpm_model()
    conc_lpm_model(pm,tm,pars)

    