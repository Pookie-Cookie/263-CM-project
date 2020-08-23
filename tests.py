import calibration
import data_prep_functions as dpf
import lpm_solving_functions as lsf
import ode_functions
import onehunga_aquifer

def test_extraction_unit_conversion():
    try:
        assert(dpf.extraction_unit_convert(1000) - 2.739726027 > 0.001)
    except(AssertionError):
        print("extraction_unit_conversion function from data prep functions aint right")
    print('potato')

test_extraction_unit_conversion()