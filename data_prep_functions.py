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

        Forgotten how to load data from a file? Review datalab under Files/cm/
        engsci233 on the ENGSCI263 Canvas page.
    '''
    #read data in from csv
    data=np.genfromtxt(fname="ac_p.csv",delimiter=',',skip_header=True)
    #first col - time vals, second col - temp. vals
    t=data[:,0]
    P=data[:,1]

    return t,P

def interpolate_extraction(t,tv,qv):
    ''' Return extraction parameter q for Onehunga Aquifer.

        Parameters:
        -----------
        t : array-like
            Vector of times at which to interpolate the extraction rate.
        tv : array-like
            Vector of times for which extraction rate is known.
        qv : array-like
            Vector of measured extraction rates.

        Returns:
        --------
        q : array-like
            Extraction rate (megalitres/day) interpolated at t.

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
    #Desnity of water extracted assumed to be 997 kg/m^3 
    q=(q_data/365)*0.997

    return q

def pressure_unit_convert(p_data):
    ''' Convert pressure data values to time-in-years units

        Parameters:
        -----------
        p_data : array-like
            Vector of pressure values in MPa

        Returns:
        --------
        q : array-like
            Vector of pressure in kg/m*year^2
    '''
    #1000 m^3 in a megalitre
    p=p_data*10**6*(365*24*60**2)**2

    return p




