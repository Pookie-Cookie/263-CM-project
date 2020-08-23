import calibration
import data_prep_functions as dpf
import lpm_solving_functions as lsf
import ode_functions
import onehunga_aquifer
import numpy as np

def test_extraction_unit_conversion():
    try:
        assert(dpf.extraction_unit_convert(1000) - 2.739726027 > 0.001)
    except(AssertionError):
        print("extraction_unit_conversion function from data prep functions aint right")


def test_pressure_unit_convert():
    try:
        assert(dpf.pressure_unit_convert())
    except(AssertionError):
        print("data_prep_functions pressure_unit_convert function not right")
        

def test_conc_unit_convert():
    try:
        assert(dpf.conc_unit_convert())
    except(AssertionError):
        print("data_prep_functions conc_unit_convert function not right")


def test_pressure_ode():
    try:
        assert(ode_functions.pressure_ode(1, 2, 3, 4, 5, 6) == 30)
    except(AssertionError):
        print("ode_functions pressure_ode function not implemented correctly")

test_pressure_ode()