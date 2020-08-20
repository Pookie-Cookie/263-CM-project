# ENGSCI263: Gradient Descent Calibration
# main.py

# PURPOSE:
# To IMPLEMENT and TEST a gradient descent calibration method.

# PREPARATION:
# Notebook calibration.ipynb.

# SUBMISSION:
# Show the instructor that you can produce the final figure in the lab document.

# import modules and functions
import numpy as np
from gradient_descent import obj_dir,step,line_search
#from wellbore_model import *
#from wellbore_model import wellbore_obj as obj2
#from plotting import *

# import pressure residual function as objective function to test
from gradient_descent import pressure_obj as obj


# **this function is incomplete**
#					 ----------
def main():
    # TASK ONE: COMPUTE STEEPEST DESCENT DIRECTION
    # 1. complete the function obj_dir in gradient_descent.py
    # 2. run this section of code to the 'return' statement
    # 3. check that the generated plot is the same as the lab document
    # 4. comment the 'return' and 'plot_s' commands and move on
    
    # parameter vector - initial guess of minimum location
    #theta0 = np.array([.5, -.5])

    # parameter vector - initial guess of minimum location
    #theta0=np.array([0.0001,0.0001,-0.05,0.05])
    #theta0=np.array([0.00055,0.15984,-0.04974,0.060258])
    theta0=np.array([0.00055,0.15984,-0.04974,0.070258,0.0801])
    
    # compute steepest descent direction
    s0 = obj_dir(obj, theta0)
    # plot 1: compare against lab2_instructions.pdf, Figure 1 
    #plot_s0(obj, theta0, s0)
    # exit function
    #return



    # TASK TWO: TAKE STEP IN STEEPEST DESCENT DIRECTION
    # 1. complete the function step in gradient_descent.py
    # 2. run this section of code to the 'return' statement
    # 3. check that the generated plot is the same as the lab document
    # 4. comment the 'return' and 'plot_step' commands and move on
    
    # choose step size 
    alpha = 0.6
    # update parameter estimate
    theta1 = step(theta0, s0, alpha)
    # plot 2: compare against lab2_instructions.pdf, Figure 2 
    #plot_step(obj, theta0, s0, theta1) 
    # exit function
    #return



    # TASK THREE: COMPUTE STEEPEST DESCENT DIRECTION AT THE UPDATED PARAMETER
    # 1. complete the command below
    # 2. run this section of code to the 'return' statement
    # 3. check that the generated plot is the same as the lab document
    # 4. comment the 'return' and 'plot_s1' commands and move on
    
    # Get the new Jacobian for the last parameters estimation
    # **uncomment and complete the command below**
    s1 = obj_dir(obj,theta1)

    # plot 3: compare against lab2_instructions.pdf, Figure 3 
    #plot_s1(obj, theta0, s0, theta1, s1) 
    # exit function
    #return



    # TASK FOUR: COMPLETE STEEPEST DESCENT ALGORITHM
    # 1. complete the loop commands below
    # 2. run this section of code to the 'return' statement
    # 3. check that the generated plot is the same as the lab document
    # 4. comment the 'return' and 'plot_steps' commands and move on
    
    # Plot iterations
    # The following script repeats the process until an optimum is reached, or until the maximum number of iterations allowed is reached
    # Try with different gammas to see how it impacts the optimization process 
    # Uncomment line 47 to use a line search algorithm
    theta_all = [theta0]
    s_all = [s0]
    # iteration control
    N_max = 50
    N_it = 0
    # begin steepest descent iterations
        # exit when difference in s reaches some small amount
    while N_it < N_max:
    #while (len(s_all)<2) or (abs(s_all[-1]-s_all[-2]) < 1.e-6) :
        # uncomment line below to implement line search (TASK FIVE)
        alpha = line_search(obj, theta_all[-1], s_all[-1])
        
        # update parameter vector 
        # **uncomment and complete the command below**
        theta_next = step(theta0,s0,alpha)
        theta_all.append(theta_next) 	# save parameter value for plotting
        
        # compute new direction for line search (thetas[-1]
        # **uncomment and complete the command below**
        s_next = obj_dir(obj,theta_next)
        s_all.append(s_next) 			# save search direction for plotting
        
        # compute magnitude of steepest descent direction for exit criteria
        N_it += 1
        # restart next iteration with values at end of previous iteration
        theta0 = 1.*theta_next
        s0 = 1.*s_next
    
    print('Optimum: ', round(theta_all[-1][0], 2), round(theta_all[-1][1], 2))
    print('Number of iterations needed: ', N_it)

    # plot 4: compare against lab2_instructions.pdf, Figure 4 
    #plot_steps(obj, theta_all, s_all)
    # exit function
    #return



    # TASK FIVE: USE LINE SEARCH
    # 1. in the code above, uncomment the line 'alpha = ...' 
    # 2. run this section of code to again
    # 3. check that the generated plot is the same as the lab document
    # 4. comment the 'return' and 'plot_steps' commands and move on



    # TASK SIX: CALIBRATE A GEOTHERMAL WELLBORE MODEL
    # 1. comment the command 'main()' at the bottom of this file
    # 2. uncomment the command 'calibrate_wellbore()' 
    # 3. run the code again to automatically calibrate a wellbore model
    # 4. inspect the SAVED plots lab2_plot5_iteration_*i*.png
    # 5. rerun the calibration using the different starting guesses
    

# this function is complete
def calibrate_wellbore():

    # indicate start of the auto calibration process
    print('\nBeginning auto-calibration of the wellbore model...')

    # choose step size
    alpha = 0.03

    # parameter vector - initial guess at optimum (reservoir pressure in bars, steam
    # fraction in [0 - 1]
    theta0 = np.array([112., .06])
    #theta0 = np.array([95., .35])
    #theta0 = np.array([120., .40])

    # change the parameter space to have those limited between 0 and 1 
    X0 = transf0(theta0)
    
    # estimate the objective function at X_next
    s0 = obj2(X0)
    
    # compute steepest descent direction
    s = obj_dir(obj2, X0)
    
    # save successive parameter values in a vector
    theta_all = [theta0]

    # plot the first parameter vector
    plot_steps_wellbore(theta_all, s0)

    # iteration control
    N_max = 25
    N_it = 1

    # compute first guess
    X_next = step(X0, s, alpha)

    # estimate the objective function at X_next
    s_next = obj2(X_next)

    # begin steepest descent iterations
        # exit when (i) new calculated objective function is higher than the previous, or (ii) max iterations exceeded
    while s0 > s_next and N_it < N_max:
        # update parameter vector
        theta_all.append(transf1(X_next))

        # output iteration number
        print('Iteration '+str(N_it))

        # plot the new estimate
        plot_steps_wellbore(theta_all, s_next)

        # restart next iteration with values at end of previous iteration
        X0 = 1.*X_next
        s0 = 1.*s_next

        # compute new direction for line search
        s = obj_dir(obj2, X0)

        # update parameter estimate 
        X_next = step(X0, s, alpha)

        # update objective function optimization for exit criteria
        s_next = obj2(X_next)
        N_it += 1
        
    # print to screen information for user 
    if N_it == N_max:
        print('Maximum number of iterations reached!')
    else:
        print('Optimum: '+str(round(theta_all[-1][0], 2))+' bars, '+str(round(theta_all[-1][1]*100, 2))+'% steam')
        print('Number of iterations needed: ', N_it-1)	


# The code below says:
#
# "If this Python file is executed as the command line, i.e., 
#            'python main.py' 
# then ONLY execute the commands below 'if __name__ == "__main__":' "
#
# "Those commands can 'call out' to OTHER functions defined in this file, e.g., main"
#
# Basically, its a convenient way to turn your script to a function and develop it incrementally.
if __name__ == "__main__":
    main()

    #calibrate_wellbore()