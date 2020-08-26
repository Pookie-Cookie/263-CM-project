#Contains functions for loading data and preparing them for numerical solution in ode functions
#Refer to lab 2 for similar examples

import numpy as np
from scipy.interpolate import interp1d


#############################################################################################
#DATA LOADING
#############################################################################################

def load_extraction_rates():
    ''' Returns time and extraction measurements from extraction csv file.

        Parameters:
        -----------
        none

        Returns:
        --------
        t : array-like
            Vector of times (years) at which measurements were taken.
        Q : array-like
            Vector of extraction measurements.

        Notes:
        ------
        The file name of file containing the data is hard coded inside this function.

        Forgotten how to load data from a file? Review datalab under Files/cm/
        engsci233 on the ENGSCI263 Canvas page.
    '''
    #read data in from csv
    data=np.genfromtxt(fname="ac_q.csv",delimiter=',',skip_header=True)
    #first col - time vals, second col - temp. vals
    t=data[:,0]
    Q=data[:,1]

    return t,Q

def load_pressures():
    ''' Returns time and pressure measurements from pressure csv file.

        Parameters:
        -----------
        none

        Returns:
        --------
        t : array-like
            Vector of times (years) at which measurements were taken.
        P : array-like
            Vector of pressure measurements.

        Notes:
        ------
        The file name of file containing the data is hard coded inside this function.
    '''
    #read data in from csv
    data=np.genfromtxt(fname="ac_p.csv",delimiter=',',skip_header=True)
    #first col - time vals, second col - temp. vals
    t=data[:,0]
    P=data[:,1]

    return t,P

def load_concs():
    ''' Returns time and conc measurements from conc csv file.

        Parameters:
        -----------
        none

        Returns:
        --------
        t : array-like
            Vector of times (years) at which measurements were taken.
        C : array-like
            Vector of conc measurements.

        Notes:
        ------
        The file name of file containing the data is hard coded inside this function.
    '''
    #read data in from csv
    data=np.genfromtxt(fname="ac_cu.csv",delimiter=',',skip_header=True)
    #first col - time vals, second col - temp. vals
    t=data[:,0]
    C=data[:,1]

    return t,C

def interpolate_forcer_linker(t,tv,qv):
    ''' Return forcing or linking variable q or p for Onehunga Aquifer.

        Parameters:
        -----------
        t : array-like
            Vector of times at which to interpolate the variable.
        tv : array-like
            Vector of times for which the variable is known.
        qv : array-like
            Vector of known values for variable.

        Returns:
        --------
        q : array-like
            Extraction rate (megalitres/day) or pressure[MPa] interpolated at t.

        Notes:
        ------
        Spline interpolation is used to interpolate the data
    '''
    q_splines=interp1d(tv,qv,kind='cubic')
    #interp1d creates a function which can be fed interpolation points stored in t
    return q_splines(t)

#############################################################################################
#UNIT CONVERTERS
#############################################################################################

def extraction_unit_convert(q_data):
    ''' Convert extractions data values to mass rate units

        Parameters:
        -----------
        q_data : array-like
            Vector of extraction values in megalitres per day

        Returns:
        --------
        q : array-like
            Vector of extraction rates in kg/year
    '''
    #Density of water extracted assumed to be 1000 kg/m^3 
    q=(q_data/365)

    return q



def conc_unit_convert(c_data):
    ''' Convert copper concentration into mass fraction

        Parameters:
        -----------
        c_data : array-like
           Vector of conc values in mg/L

        Returns:
        --------
        c : array-like
            Vector of conc in mass fraction (as a fraction of the entire aquifer mass)
    '''
    #assume density of water 1000kg/m^3
    c=(c_data)*(1.e-6)
    
    return c    



