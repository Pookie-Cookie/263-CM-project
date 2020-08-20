#Contains the ode functions and data loading needed for numerical solutions to LPMs
#Refer to lab 2 for similar examples

#from scipy.misc import derivative
from scipy.interpolate import interp1d
from data_prep_functions import load_extraction_rates

def pressure_ode(t, p, q, a, b, p0, p1):
    ''' Return the derivative dP/dt at time, t, for given parameters.

        Parameters:
        -----------
        t : float
            time(independent variable).
        p : float
            pressure(dependent variable).
        q : float
            Extraction rate.
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
            Derivative of pressure with respect to time.

        Notes:
        ------
        Based on D.Dempsey's LPM formulation for the Onehunga Aquifer.
        Extraction rate must be in units m^3/year

        Examples:
        ---------
        >>> pressure_model(0, 1, 2, 3, 4, 5, 6)
        30

    '''
    return -a*q-b*(p-p0)-b*(p-p1)  

def low_pressure_boundary(c,p,p0):
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


def conc_ode(t, c, p, a, b, p0, p1, d, m0, csrc):
    ''' Return the derivative dC/dt at time, t, for given parameters.

        Parameters:
        -----------
        t : float
            time(independent variable).
        c : float
            copper concentration(dependent variable).
        p : float
            pressure
        q : float
            Extraction rate.
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
            Derivative of concentration with respect to time.

        Notes:
        ------
        Based on D.Dempsey's LPM formulation for the Onehunga Aquifer.
        concentration c must be in units kg/kg i.e. a mass percentage

        Examples:
        ---------
        >>> conc_model(0, 1, 2, 3, 4, 5, 6)
        26.3958

    '''
    #mass flow of copper at low p. boundary depends on relative pressure
    cprime=low_pressure_boundary(c,p,p0)
    #find m0*dc/dt
    mdcdt=-(b/a)*(p-p0)*(cprime-c)+(b/a)*(p-p1)*c-d*(p-((p0+p1)/2))*csrc

    return mdcdt/m0



