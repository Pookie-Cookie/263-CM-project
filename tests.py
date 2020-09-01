import solve_calibrate as sc
import data_prep_functions as dpf
import numpy as np
import lpm_solve as ls
from scipy.linalg import norm


def test_extraction_unit_conversion():
    #test basic conversion
    try:
        assert(dpf.extraction_unit_convert(1) - 2.739726027e-3 < 0.001)
    except(AssertionError):
        print("extraction_unit_conversion function from data prep functions aint right")

    #test np arrays
    try:
        input = np.array([1, 1, 0, 20])
        assert(np.linalg.norm(dpf.extraction_unit_convert(input) - [2.739726027e-3, 2.739726027e-3, 0, 0.05479452055]) < 0.001)
    except(AssertionError):
        print("extraction_unit_conversion function from data prep functions has problems with np arrays")      


def test_conc_unit_convert():
    #test individual input
    try:
        assert(dpf.conc_unit_convert(1) - 1.e-6 < 0.001)
    except(AssertionError):
        print("data_prep_functions conc_unit_convert function not right")
    
    #test array input
    try:
        input = np.array([1, 0, 2, 1])
        assert(np.linalg.norm(dpf.conc_unit_convert(input) - [1.e-6, 0, 2.e-6, 1.e-6]) < 0.001)
    except (AssertionError):
        print("data_prep_functions conc_unit_convert function not right with array inputs")


def test_p_lpm():
    try:
        assert(ls.p_lpm(0, 1, 2, 3, 4, 5)-30 < 0.001)
        print("alg here")
    except(AssertionError):
        print("p_lpm isnt right")
        
def test_solve_p_lpm():
    try: 
        assert(norm(ls.solve_p_lpm([1, 2, 3, 4, 5],1,2,20,40)-[0.03129011, 0.03129011, 0.03129011, 0.03129011, 0.03129011]) < 0.001)
        print("function appears to be working fine")
    except(AssertionError):
        print("something wrong with the pressure ODE numerical solver")


def test_c_lpm():
    try:
        assert(ls.c_lpm(0, 1, 2, 3, 4, 5, 6, 7, 8)-30.643 < 0.001)
        print("c_lpm is working fine")
    except(AssertionError):
        print("c_lpm isnt right")

def test_solve_c_lpm():
    try:
        assert(norm(ls.solve_c_lpm([1, 2, 3, 4, 5], 1, 2, 3, 4, 5, 6, 7) - [0, 0, 0, 0, 0]) < 0.001)
        print("solve_c_lpm is working fine")
    except(AssertionError):
        print("solve_c_lpm isnt working right")
        