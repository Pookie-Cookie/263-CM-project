import matplotlib.pyplot as plt
import numpy as np

#data
yearCu = [1980,1985,1990,1995,2000,2005,2010,2015]
concCu = [0.00E+00,1.30E-02,1.48E-01,3.52E-01,5.43E-01,8.19E-01,8.88E-01,9.76E-01]
yearPa = np.arange(1980,2018,2)
valsPa = [3.13E-02, 1.05E-02, -1.13E-03, -8.18E-03, -2.00E-02, -3.91E-02, -3.89E-02, -4.79E-02, -5.01E-02, -5.15E-02, -5.37E-02, -4.37E-02, -4.19E-02, -4.06E-02, -3.65E-02, -3.46E-02, -2.85E-02, -3.29E-02, -2.98E-02]
yearEx = np.arange(1980, 2019)
valsEx = [3.15E+01,3.24E+01,3.34E+01,3.41E+01,3.29E+01,3.47E+01,3.50E+01,3.67E+01,3.76E+01,3.71E+01,3.67E+01,3.60E+01,3.52E+01,3.51E+01,3.49E+01,2.95E+01,3.23E+01,3.40E+01,3.54E+01,3.63E+01,1.84E+01,1.88E+01,1.93E+01,1.91E+01,1.95E+01,1.88E+01,1.85E+01,1.90E+01,1.91E+01,1.92E+01,1.88E+01,1.95E+01,1.84E+01,1.86E+01,1.92E+01,1.81E+01,1.91E+01,1.70E+01,1.72E+01]

f,(ax1,ax3)=plt.subplots(nrows=1,ncols=2,figsize=(7,4),constrained_layout=True)
ax2=ax1.twinx()
ax4=ax3.twinx()

#plot extraction cf pressure vs time
ax1.plot(yearEx,valsEx, 'b', label='extraction rate')
ax2.plot(yearPa,valsPa,'--k',label='pressure')


#plot pressure cf cu vs time
ax3.plot(yearPa,valsPa,'--k',label='_pressure')
ax4.plot(yearCu,concCu,'ro',label='Cu concentration')


#restrict axes
ax1.set_xlim([1980,2018])
ax3.set_xlim([1980,2016])
ax4.set_xlim([1980,2016])

#set figure and axes labels
#ax1.legend(loc=4)
#ax2.legend(loc=4)
#ax3.legend(loc=4)
#ax4.legend(loc=4)

f.legend(loc="upper left", fontsize=6 ,bbox_to_anchor=(1.1,1.02),bbox_transform=ax1.transAxes)

ax1.set_xlabel('time [yr]')
ax3.set_xlabel('time [yr]')

ax1.set_ylabel('Extraction rate [$10^6$ litre/day]')
ax3.set_ylabel('Pressure [MPa]')

ax2.set_ylabel('Pressure [MPa]')
ax4.set_ylabel('Dissolved Cu concentration [mg/litre]')

ax1.set_title('Comparison of extraction rate and pressure',size=7)
ax4.set_title('Comparison of pressure and copper concentration',size=7)
f.suptitle('Variation in Onehunga Aquifer pressure and copper concentration over a 40-year period',size=10)

#f.set_tight_layout(True)

#f.subplots_adjust(wspace=0.9)

save_figure = True
if not save_figure:
	#Open a new window and display the plot
	plt.show()
else:
	#Save that plot to a png file
	plt.savefig('extract_pressure_cu.png',dpi=300)