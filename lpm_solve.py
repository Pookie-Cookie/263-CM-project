from data_prep_functions import *

# define derivative function
def p_lpm(p,t,a,b,p0,p1):            
    
    # load flow rate data
    tq,qi = load_extraction_rates()
    qi = extraction_unit_convert(qi)
    # interpolate (piecewise linear) flow rate
    q = np.interp(t,tq,qi)           
    
    # compute derivative
    return -a*q-b*(p-p0)-b*(p-p1)

# implement an imporved Euler step to solve the ODE
def solve_p_lpm(t,a,b,p0,p1):

    # load pressure data
    tp,p = load_pressures()
    # initial value
    pm = [p[0],]                            
    # solve at pressure steps
    for t0,t1 in zip(tp[:-1],tp[1:]):          
        # predictor gradient
        dpdt1 = p_lpm(pm[-1]-p[0], t0, a, b, p0, p1)
        # predictor step
        pp = pm[-1] + dpdt1*(t1-t0)
        # corrector gradient             
        dpdt2 = p_lpm(pp-p[0], t1, a, b, p0, p1)
        # corrector step       
        pm.append(pm[-1] + 0.5*(t1-t0)*(dpdt2+dpdt1))
    
    # interp onto requested times  
    return np.interp(t, tp, pm)

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
    # interpolate pressure from solution (FOR TESTING - run this function in an environment where tp, pm defined)
    tp, pm = load_p_lpm_solution()
    p = np.interp(t,tp,pm)           
    # find conc at low pressure boundary
    cprime=low_p_bound(c,p,p0)
    #find m0*dc/dt
    mdcdt=-(b/a)*(p-p0)*(cprime-c)+(b/a)*(p-p1)*c-d*(p-((p0+p1)/2))*csrc
    #compute derivative
    return mdcdt/m0

# implement an improved Euler step to solve the ODE
def solve_c_lpm(t,a,b,p0,p1,d,m0,csrc):
    #load conc data
    tc,c = load_concs()
    # convert to mass fraction
    c = conc_unit_convert(c)
    # initial value
    cm = [c[0],]
    # solve at conc steps                           
    for t0,t1 in zip(tc[:-1],tc[1:]):
        # predictor gradient
        dcdt1 = c_lpm(cm[-1]-c[0], t0, a, b, p0, p1, d, m0, csrc)
        # predictor step
        cp = cm[-1] + dcdt1*(t1-t0)             
        # corrector gradient
        dcdt2 = c_lpm(cp-c[0], t1, a, b, p0, p1, d, m0, csrc)
        # corrector step
        cm.append(cm[-1] + 0.5*(t1-t0)*(dcdt2+dcdt1))
    
    #interp onto requested times
    return np.interp(t, tc, cm)                   