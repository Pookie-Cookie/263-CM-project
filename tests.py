import solve_calibrate as sc
import data_prep_functions as dpf
import numpy as np
import lpm_solve as ls


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




def test_pressure_unit_convert():
    #test single input
    try:
        assert(dpf.pressure_unit_convert(1) - 9.94519296e20 < 0.000001)
        print("pressure unit convert is good")
    except(AssertionError):
        print("data_prep_functions pressure_unit_convert function not right")
    
    #test with array inputs
    try:
        input = np.array([0, 1, 1, 2])
        assert(np.linalg.norm(dpf.pressure_unit_convert(input) - [0, 9.94519296e20, 9.94519296e20, 1.989038592e21]) < 0.000001)
    except (AssertionError):
        print("pressure unit convert array input error")
        



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
        assert(sc.conc_lpm_model.c_lpm(0, 1, 2, 3, 4, 5)-30 < 0.001)
        print("alg here")
    except(AssertionError):
        print("p_lpm isnt right")

test_p_lpm()