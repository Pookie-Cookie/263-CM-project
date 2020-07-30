import matplotlib.pyplot as plt
import numpy as np

year = [1980,1985,1990,1995,2000,2005,2010,2015]
dissolved_Cu = [0.00E+00,1.30E-02,1.48E-01,3.52E-01,5.43E-01,8.19E-01,8.88E-01,9.76E-01]
fig = plt.plot(year, dissolved_Cu, 'bo', year, dissolved_Cu, 'b')
plt.xlabel('year')
plt.ylabel('dissovled Cu [mg/litre]')
plt.title('dissovled Cu [mg/litre] from 1980-2015')
plt.show()


year = np.arange(1980, 2018, 2)
pressure = [3.13E-02, 1.05E-02, -1.13E-03, -8.18E-03, -2.00E-02, -3.91E-02, -3.89E-02, -4.79E-02, -5.01E-02, -5.15E-02, -5.37E-02, -4.37E-02, -4.19E-02, -4.06E-02, -3.65E-02, -3.46E-02, -2.85E-02, -3.29E-02, -2.98E-02]
fig = plt.plot(year, pressure, 'bo', year, pressure, 'b')
plt.xlabel('year')
plt.ylabel('pressure [MPa]')
plt.title('pressure [MPa] from 1980-2016')
plt.show()


year = np.arange(1980, 2019)
extraction = [3.15E+01,3.24E+01,3.34E+01,3.41E+01,3.29E+01,3.47E+01,3.50E+01,3.67E+01,3.76E+01,3.71E+01,3.67E+01,3.60E+01,3.52E+01,3.51E+01,3.49E+01,2.95E+01,3.23E+01,3.40E+01,3.54E+01,3.63E+01,1.84E+01,1.88E+01,1.93E+01,1.91E+01,1.95E+01,1.88E+01,1.85E+01,1.90E+01,1.91E+01,1.92E+01,1.88E+01,1.95E+01,1.84E+01,1.86E+01,1.92E+01,1.81E+01,1.91E+01,1.70E+01,1.72E+01]
fig = plt.plot(year, extraction, 'bo', year, extraction, 'b')
plt.xlabel('year')
plt.ylabel('extraction [10^6 litre/day]')
plt.title('extraction [10^6 litre/day] from 1980-2018')
plt.show()