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
<<<<<<< HEAD
        assert(norm(ls.solve_p_lpm([1, 2, 3, 4, 5],1,2,20,40)-[0.03129011, 0.03129011, 0.03129011, 0.03129011, 0.03129011]) < 0.001)
=======
        assert(np.linalg.norm(ls.solve_p_lpm([1, 2, 3, 4, 5],1,2,20,40)-[0.03129011, 0.03129011, 0.03129011, 0.03129011, 0.03129011]) < 0.001)
>>>>>>> 83e3a5632ff784f156c7e05f2817acdc7593e117
        print("function appears to be working fine")
    except(AssertionError):
        print("something wrong with the pressure ODE numerical solver")


<<<<<<< HEAD
def test_c_lpm():
    try:
        assert(ls.c_lpm(0, 1, 2, 3, 4, 5, 6, 7, 8)-30.643 < 0.001)
        print("c_lpm is working fine")
    except(AssertionError):
        print("c_lpm isnt right")

def test_solve_c_lpm():
    try:
        print(ls.solve_c_lpm([1, 2, 3, 4, 5], 1, 2, 3, 40, 5, 6, 7))
        assert(norm(ls.solve_c_lpm([1, 2, 3, 4, 5], 1, 2, 3, 4, 5, 6, 7) - [0, 0, 0, 0, 0]) < 0.001)
        print("solve_c_lpm is working fine")
    except(AssertionError):
        print("solve_c_lpm isnt working right")
        
test_solve_c_lpm()
=======
if __name__ == "__main__":
    test_extraction_unit_conversion()
    test_conc_unit_convert()
    test_p_lpm()
    test_solve_p_lpm()
        
>>>>>>> 83e3a5632ff784f156c7e05f2817acdc7593e117
