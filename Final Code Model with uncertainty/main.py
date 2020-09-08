# Run this file to generate all the plots associated with Group 10's reports.
# Please set any plotting functions inputs to true to save the plot to disk.

#IMPORTS
from data_describe_functions import *
from benchmarking import *
from tests import *
from solve_calibrate import *
from solve_predict import *

# GIVEN ?
# initial data visualisation/description:

# show seperate comparisons of data
separate_compare(save=False)
# show extraction - pressure - copper link
extract_pressure_cu(save=False)

# FORMULATE ? / WORKING ?
# Benchmarking and convergence:
plot_pressure_benchmark(save=False)
plot_conc_benchmark(save=False)

# Unit testing:
# N.B. these print test result to screen
test_extraction_unit_convert()
test_conc_unit_convert()
test_p_lpm()
test_solve_p_lpm()
test_c_lpm()    
test_solve_c_lpm()

# SUITABLE ?
# Calibrate the model to known data

pm, tm, pars = pressure_lpm_model(save=False) # this MUST be run before calling either conc_lpm_model or conc_lpm_predict
conc_lpm_model(pm,tm,pars,save=False)

# USE ?
# Predict outcomes depending on extraction rate
levels=[0, 10, 20, 40]
pm, tm, pars = pressure_lpm_predict(levels, 2050) # this MUST be run beofre calling conc_lpm_predict
conc_lpm_predict(pm,tm,pars,levels, save=False)

# UNKNOWN ?
# Find range of outcomes depending on uncertaintly in data to calibrate to
conc_lpm_uncertain(pm,tm,pars,levels, save=False)

# RESET files in working directory
# restore historical data in ac_q.csv
q_reset()
import os

# remove pressure solution for existing data
if os.path.exists('p_lpm_soln.txt'):
    os.remove('p_lpm_soln.txt')
else:
    print("The file does not exist")

# remove files for future/extrapolated solutions
for level in levels:
    if os.path.exists('p_soln_q_{:d}.txt'.format(level)):
        os.remove('p_soln_q_{:d}.txt'.format(level))
    else:
        print("The file does not exist")

