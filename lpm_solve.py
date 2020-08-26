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