from data_prep_functions import *

# define derivative function
def p_lpm(p,t,a,b,p0,p1):
    ''' Return the derivative dP/dt at time, t, for given parameters.

        Parameters:
        -----------
        p : float
            pressure(dependent variable).
        t : float
            time(independent variable).
        a : float
            low pressure boundary recharge parameter.
        b : float
            high pressure boundary recharge parameter.
        p0 : float
            low pressure boundary pressure parameter.
        p1 : float
            high pressure boundary pressure parameter.        

        Returns:
        --------
        dpdt : float
            Derivative of pressure with respect to time, at time t.

        Notes:
        ------
        Based on D.Dempsey's LPM formulation for the Onehunga Aquifer.
        Extraction rate must be in units m^3/year

        Examples:
        ---------
        >>> pressure_model(0, 1, 2, 3, 4, 5, 6)
        30
    '''            
    
    # load flow rate data
    tq,qi = load_extraction_rates()
    qi = extraction_unit_convert(qi)
    # interpolate (piecewise linear) flow rate
    q = np.interp(t,tq,qi)           
    
    # compute derivative
    return -a*q-b*(p-p0)-b*(p-p1)

# implement an imporved Euler step to solve the ODE
def solve_p_lpm(t,a,b,p0,p1):
    ''' Solve an ODE numerically for the Onehunga Aquifer system

        Parameters:
        -----------
        t : float
            times for which solution is needed.
        a : float
            low pressure boundary recharge parameter.
        b : float
            high pressure boundary recharge parameter.
        p0 : float
            low pressure boundary pressure parameter.
        p1 : float
            high pressure boundary pressure parameter.   

        Returns:
        --------
        p_soln : array-like
            Dependent variable solution vector corresponding to times in t.

        Notes:
        ------
        ODE is solved using the Improved Euler Method.
        A pressure csv file called ac_p.csv MUST be present in
        the working directory for this function to run. 

        Assume that ODE function f takes the following inputs, in order:
            1. dependent variable
            2. independent variable
            3. other parameters
    '''

    # load pressure data - to get the initial value
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
    ''' Return the copper conc in the flux at the low pressure boundary
        
        Parameters:
        -----------
        c : float
            concentration 
        p : float
            pressure
        p0 : float
            low pressure boundary pressure parameter.
                    
        Returns:
        --------
        cprime : float
            copper concentration in flux at low pressure boundary

        Notes:
        ------
        Based on D.Dempsey's LPM formulation for the Onehunga Aquifer.
        concentration c must be in units kg/kg i.e. a mass percentage.
        
        If flux inflow occurs, no copper comes in at the low pressure boundary
        If flux outflow occurs, copper leaves at the same conc. as the aquifer

        Examples:
        ---------
        >>> low_pressure_boundary(1, 2, 3)
        0
    '''
    if p>p0:
        # contaminated water outflow happens when pressure greater inside aquifer than
        # at low pressure boundary    
        return c
    else:
        return 0

# define derivative function
def c_lpm(c,t,a,b,p0,p1,d,m0,csrc):
    ''' Return the derivative dC/dt at time, t, for given parameters.

        Parameters:
        -----------
        c : float
            copper concentration(dependent variable).
        t : float
            time(independent variable).
        a : float
            low pressure boundary recharge parameter.
        b : float
            high pressure boundary recharge parameter.
        p0 : float
            low pressure boundary pressure parameter.
        p1 : float
            high pressure boundary pressure parameter.        
        d : float
            stormwater surface leaching parameter.
        m0 : float
            total aquifer mass parameter. 
        csrc : float
            surface leaching stormwater concentration parameter.          
        
        Returns:
        --------
        dcdt : float
            Derivative of concentration with respect to time, at time t.

        Notes:
        ------
        Based on D.Dempsey's LPM formulation for the Onehunga Aquifer.
        concentration c must be in units kg/kg i.e. a mass percentage.
        pressure_lpm_model() MUST be run and MUST generate a csv file 
        containing the pressure solution before this function can be used.

        Examples:
        ---------
        >>> conc_model(0, 1, 2, 3, 4, 5, 6)
        26.3958
    '''                
    # interpolate pressure from solution 
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
    ''' Solve the conc ODE numerically for the Onehunga Aquifer system

        Parameters:
        -----------
        t : float
            times for which solution is needed.
        a : float
            low pressure boundary recharge parameter.
        b : float
            high pressure boundary recharge parameter.
        p0 : float
            low pressure boundary pressure parameter.
        p1 : float
            high pressure boundary pressure parameter.   
        d : float
            stormwater surface leaching parameter.
        m0 : float
            total aquifer mass parameter. 
        csrc : float
            surface leaching stormwater concentration parameter.   

        Returns:
        --------
        c_soln : array-like
            Dependent variable solution vector corresponding to times in t.

        Notes:
        ------
        ODE is solved using the Improved Euler Method. 

        Assume that ODE function f takes the following inputs, in order:
            1. dependent variable
            2. independent variable
            3. other parameters
    '''
    #load conc data - to get intial value
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