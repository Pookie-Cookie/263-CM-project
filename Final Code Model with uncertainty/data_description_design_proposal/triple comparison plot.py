import numpy as np
import matplotlib.pyplot as plt

yearPa = np.arange(1980,2018,2)
yearCu=[1980,1985,1990,1995,2000,2005,2010,2015]
yearExtr = np.arange(1980, 2019)
extraction = [3.15E+01,3.24E+01,3.34E+01,3.41E+01,3.29E+01,3.47E+01,3.50E+01,3.67E+01,3.76E+01,3.71E+01,3.67E+01,3.60E+01,3.52E+01,3.51E+01,3.49E+01,2.95E+01,3.23E+01,3.40E+01,3.54E+01,3.63E+01,1.84E+01,1.88E+01,1.93E+01,1.91E+01,1.95E+01,1.88E+01,1.85E+01,1.90E+01,1.91E+01,1.92E+01,1.88E+01,1.95E+01,1.84E+01,1.86E+01,1.92E+01,1.81E+01,1.91E+01,1.70E+01,1.72E+01]
pressure = [3.13E-02, 1.05E-02, -1.13E-03, -8.18E-03, -2.00E-02, -3.91E-02, -3.89E-02, -4.79E-02, -5.01E-02, -5.15E-02, -5.37E-02, -4.37E-02, -4.19E-02, -4.06E-02, -3.65E-02, -3.46E-02, -2.85E-02, -3.29E-02, -2.98E-02]
dissolved_Cu = [0.00E+00,1.30E-02,1.48E-01,3.52E-01,5.43E-01,8.19E-01,8.88E-01,9.76E-01]


fig, host = plt.subplots()
fig.subplots_adjust(right = 0.75)

par1 = host.twinx()
par2 = host.twinx()
par2.spines["right"].set_position(("axes", 1.2))

p1, = host.plot(yearCu, dissolved_Cu, "b-", label="Cu concentration")
p2, = par1.plot(yearExtr, extraction, "r-", label="extraction rate")
p3, = par2.plot(yearPa, pressure, "g-", label="pressure")

host.set_xlabel("year")
host.set_ylabel("Cu concentration [mg/litre]")
par1.set_ylabel("extraction [$10^6$ litre/day]")
par2.set_ylabel("pressure [MPa]")

host.yaxis.label.set_color(p1.get_color())
par1.yaxis.label.set_color(p2.get_color())
par2.yaxis.label.set_color(p3.get_color())

tkw = dict(size=4, width=1.5)
host.tick_params(axis='y', colors=p1.get_color(), **tkw)
par1.tick_params(axis='y', colors=p2.get_color(), **tkw)
par2.tick_params(axis='y', colors=p3.get_color(), **tkw)
host.tick_params(axis='x', **tkw)

lines = [p1, p2, p3]

host.legend(lines, [l.get_label() for l in lines])

plt.show()