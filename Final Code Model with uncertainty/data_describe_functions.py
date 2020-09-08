# contains plotting functions needed for data description


import matplotlib.pyplot as plt
import numpy as np
def extract_pressure_cu(save):
	''' Plots two side by side graphs comparing extraction and pressure, pressure and copper conc

		Parameters:
		-----------
		save : Bool
			If set to true, save figure generated to working directory

		Returns:
		--------
		None

		Notes:
		------
		Onehunga Aquifer data hardcoded in this function.
	'''
	#data
	yearCu = [1980,1985,1990,1995,2000,2005,2010,2015]
	concCu = [0.00E+00,1.30E-02,1.48E-01,3.52E-01,5.43E-01,8.19E-01,8.88E-01,9.76E-01]
	yearPa = np.arange(1980,2018,2)
	valsPa = [3.13E-02, 1.05E-02, -1.13E-03, -8.18E-03, -2.00E-02, -3.91E-02, -3.89E-02, -4.79E-02, -5.01E-02, -5.15E-02, -5.37E-02, -4.37E-02, -4.19E-02, -4.06E-02, -3.65E-02, -3.46E-02, -2.85E-02, -3.29E-02, -2.98E-02]
	yearEx = np.arange(1980, 2019)
	valsEx = [3.15E+01,3.24E+01,3.34E+01,3.41E+01,3.29E+01,3.47E+01,3.50E+01,3.67E+01,3.76E+01,3.71E+01,3.67E+01,3.60E+01,3.52E+01,3.51E+01,3.49E+01,2.95E+01,3.23E+01,3.40E+01,3.54E+01,3.63E+01,1.84E+01,1.88E+01,1.93E+01,1.91E+01,1.95E+01,1.88E+01,1.85E+01,1.90E+01,1.91E+01,1.92E+01,1.88E+01,1.95E+01,1.84E+01,1.86E+01,1.92E+01,1.81E+01,1.91E+01,1.70E+01,1.72E+01]

	f,(ax1,ax3)=plt.subplots(nrows=1,ncols=2,figsize=(8,5),constrained_layout=True)
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

	save_figure = save
	if not save_figure:
		#Open a new window and display the plot
		plt.show()
	else:
		#Save that plot to a png file
		plt.savefig('extract_pressure_cu.png',dpi=300)

def separate_compare(save):
	''' Generate two seperate plots comparing extraction & pressure, pressure & conc
		
		Parameters:
		-----------
		save : Bool
			If set to true, save BOTH figures generated to working directory

		Returns:
		--------
		None

		Notes:
		------
		Onehunga Aquifer data hardcoded in this function.
	'''

	# compare extraction and pressure
	pressure = [3.13E-02, 1.05E-02, -1.13E-03, -8.18E-03, -2.00E-02, -3.91E-02, -3.89E-02, -4.79E-02, -5.01E-02, -5.15E-02, -5.37E-02, -4.37E-02, -4.19E-02, -4.06E-02, -3.65E-02, -3.46E-02, -2.85E-02, -3.29E-02, -2.98E-02]
	extraction = [3.15E+01,3.24E+01,3.34E+01,3.41E+01,3.29E+01,3.47E+01,3.50E+01,3.67E+01,3.76E+01,3.71E+01,3.67E+01,3.60E+01,3.52E+01,3.51E+01,3.49E+01,2.95E+01,3.23E+01,3.40E+01,3.54E+01,3.63E+01,1.84E+01,1.88E+01,1.93E+01,1.91E+01,1.95E+01,1.88E+01,1.85E+01,1.90E+01,1.91E+01,1.92E+01,1.88E+01,1.95E+01,1.84E+01,1.86E+01,1.92E+01,1.81E+01,1.91E+01,1.70E+01,1.72E+01]
	yearExtr = np.arange(1980, 2019)
	fig4, y1 = plt.subplots()

	year=np.arange(1980, 2018, 2)
	y1.plot(year, pressure, 'k--')
	y1.set_ylabel('Pressure [MPa]')

	y2 = y1.twinx()
	y2.plot(yearExtr, extraction, 'b')
	y2.set_ylabel('extraction [$10^6$ litre/day]')
	fig4.legend(labels = ('Pressure', 'extraction rate'), loc=4,bbox_to_anchor=(1,0.45),bbox_transform=y1.transAxes)
	plt.title('Comparison of extraction rate and pressure')

	#show the plot to the screen OR save the plot in the directory
	save_figure = save
	if not save_figure:
		#Open a new window and display the plot
		plt.show()
	else:
		#Save that plot to a png file
		plt.savefig('extraction_vs_conc.png',dpi=300)

	# compare pressure and conc

	dissolved_Cu = [0.00E+00,1.30E-02,1.48E-01,3.52E-01,5.43E-01,8.19E-01,8.88E-01,9.76E-01]
	#pressure vs conc
	yearPa = np.arange(1980,2018,2)
	yearCu=[1980,1985,1990,1995,2000,2005,2010,2015]
	fig5, y1 = plt.subplots()
	y1.plot(yearCu, dissolved_Cu, 'ro')
	y1.set_ylabel('dissolved Cu [mg/litre]')
	y2 = y1.twinx()
	y2.plot(yearPa, pressure, 'k--')
	y2.set_ylabel('pressure [MPa]')
	fig5.legend(labels = ('Cu concentration', 'pressure'), loc=4,bbox_to_anchor=(1,0),bbox_transform=y1.transAxes)
	plt.title('Comparison of pressure and Cu concentration')
	plt.tight_layout()

	#show the plot to the screen OR save the plot in the directory
	save_figure = save
	if not save_figure:
		#Open a new window and display the plot
		plt.show()
	else:
		#Save that plot to a png file
		plt.savefig('pressure_vs_conc.png',dpi=300)

