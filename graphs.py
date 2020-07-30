import matplotlib.pyplot as plt
import numpy as np

year = [1980,1985,1990,1995,2000,2005,2010,2015]
dissolved_Cu = [0.00E+00,1.30E-02,1.48E-01,3.52E-01,5.43E-01,8.19E-01,8.88E-01,9.76E-01]
fig = plt.plot(year, dissolved_Cu, 'bo', year, dissolved_Cu, 'b')
plt.xlabel('year')
plt.ylabel('dissovled Cu [mg/litre]')
plt.title('dissovled Cu [mg/litre] from 1980-2015')
plt.show()


