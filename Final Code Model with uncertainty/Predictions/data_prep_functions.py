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
        future : Bool
            Whether we are loading extraction rates into the future or not

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

def future_extraction_rates(level, endyear):
    ''' Returns time and extraction measurements for historical and future data

        Parameters:
        -----------
        level : float
            The volume rate of extraction for the duration after
        
        endyear : int
            The year up to which data should be made

        Returns:
        --------
        t : array-like
            Vector of times (years) at which data is available
        Q : array-like
            Vector of extraction rates.

        Notes:
        ------
        The file name of file containing the data is hard coded inside this function.
        The function first loads historical data, writes these and the future level of extraction
        and the future times to csv file, then reads the file and returns these. 
    '''
    th, qh = load_extraction_rates()
    historical = np.column_stack((th, qh))
    #save the pressure solution to a .txt file
    # opening a file
    fp = open('ac_q.csv','w')
    #write header
    fp.write('t[year], q[10^6 litres/day]\n')
    #enter historical extraction data
    [fp.write('{:f}, {:f}\n'.format(t,q)) for t, q in historical[:38]]

    #enter future extraction data with same spacing as historical data
    tq = np.arange(th[37]+(th[37]-th[36]), endyear, th[37]-th[36])
    q=np.full(len(tq), fill_value=level)
    [fp.write('{:f}, {:f}\n'.format(t,q)) for t, q in np.column_stack((tq, q))]
    
    fp.close()

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

def load_p_lpm_solution():
    ''' Returns time and pressure measurements for solution to pressure lpm stored in .txt file.

        Parameters:
        -----------
        none

        Returns:
        --------
        t : array-like
            Vector of times (years) at which measurements were taken.
        p : array-like
            Vector of pressure measurements.

        Notes:
        ------
        The file name of file containing the data is hard coded inside this function.
        This is used to pass in the pressure solution to the concentration LPM functions
    '''
    
    data=np.genfromtxt(fname="p_lpm_soln.txt",delimiter=',', skip_header=True)
    #first col - time vals, second col - temp. vals
    t=data[:,0]
    p=data[:,1]

    return t,p

def load_p_extrap_soln(level):
    ''' Returns time and pressure measurements for a predicted solution to pressure lpm stored in .txt file.

        Parameters:
        -----------
        level : float
            the level of future extraction being modelled.

        Returns:
        --------
        t : array-like
            Vector of times (years) at which measurements were taken.
        p : array-like
            Vector of pressure measurements.

        Notes:
        ------
        The file name of file containing the data is hard coded inside this function,
        and must be of the form p_lpm_q_n.txt, where n=level of extraction
        This is used to pass in the pressure solution to the concentration LPM functions
    '''
    
    data=np.genfromtxt(fname="p_soln_q_{:d}.txt".format(level),delimiter=',', skip_header=True)
    #first col - time vals, second col - temp. vals
    t=data[:,0]
    p=data[:,1]

    return t,p


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



