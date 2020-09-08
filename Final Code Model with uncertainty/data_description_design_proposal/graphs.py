import matplotlib.pyplot as plt
import numpy as np
#conc over time
year = [1980,1985,1990,1995,2000,2005,2010,2015]
dissolved_Cu = [0.00E+00,1.30E-02,1.48E-01,3.52E-01,5.43E-01,8.19E-01,8.88E-01,9.76E-01]
fig1 = plt.plot(year, dissolved_Cu, 'bo', year, dissolved_Cu, 'b')
plt.xlabel('year')
plt.ylabel('dissovled Cu [mg/litre]')
plt.title('dissovled Cu [mg/litre] from 1980-2015')
plt.show()

#pressure over time
year = np.arange(1980, 2018, 2)
pressure = [3.13E-02, 1.05E-02, -1.13E-03, -8.18E-03, -2.00E-02, -3.91E-02, -3.89E-02, -4.79E-02, -5.01E-02, -5.15E-02, -5.37E-02, -4.37E-02, -4.19E-02, -4.06E-02, -3.65E-02, -3.46E-02, -2.85E-02, -3.29E-02, -2.98E-02]
fig2 = plt.plot(year, pressure, 'bo', year, pressure, 'b')
plt.xlabel('year')
plt.ylabel('pressure [MPa]')
plt.title('pressure [MPa] from 1980-2016')
plt.show()

#extraction over time
year = np.arange(1980, 2019)
extraction = [3.15E+01,3.24E+01,3.34E+01,3.41E+01,3.29E+01,3.47E+01,3.50E+01,3.67E+01,3.76E+01,3.71E+01,3.67E+01,3.60E+01,3.52E+01,3.51E+01,3.49E+01,2.95E+01,3.23E+01,3.40E+01,3.54E+01,3.63E+01,1.84E+01,1.88E+01,1.93E+01,1.91E+01,1.95E+01,1.88E+01,1.85E+01,1.90E+01,1.91E+01,1.92E+01,1.88E+01,1.95E+01,1.84E+01,1.86E+01,1.92E+01,1.81E+01,1.91E+01,1.70E+01,1.72E+01]
fig3 = plt.plot(year, extraction, 'bo', year, extraction, 'b')
plt.xlabel('year')
plt.ylabel('extraction [10^6 litre/day]')
plt.title('extraction [10^6 litre/day] from 1980-2018')
plt.show()

#extraction vs conc
yearExtr = np.arange(1980, 2019)
yearCu = [1980,1985,1990,1995,2000,2005,2010,2015]
fig4, y1 = plt.subplots()
#y1.plot(yearCu, dissolved_Cu, 'ko')
#y1.set_ylabel('dissolved Cu [mg/litre]')

year=np.arange(1980, 2018, 2)
y1.plot(year, pressure, 'k--')
y1.set_ylabel('Pressure [MPa]')

y2 = y1.twinx()
y2.plot(yearExtr, extraction, 'b')
y2.set_ylabel('extraction [$10^6$ litre/day]')
fig4.legend(labels = ('Pressure', 'extraction rate'), loc=4,bbox_to_anchor=(1,0.45),bbox_transform=y1.transAxes)
plt.title('Comparison of extraction rate and pressure')

#show the plot to the screen OR save the plot in the directory
save_figure = True
if not save_figure:
	#Open a new window and display the plot
	plt.show()
else:
	#Save that plot to a png file
	plt.savefig('extraction_vs_conc.png',dpi=300)


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
save_figure = True
if not save_figure:
	#Open a new window and display the plot
	plt.show()
else:
	#Save that plot to a png file
	plt.savefig('pressure_vs_conc.png',dpi=300)



#extraction vs pressure
fig5, y1 = plt.subplots()
y1.plot(yearExtr, extraction, 'k-')
y1.set_ylabel('extraction rate [$10^6$ litre/day]')
y2 = y1.twinx()
y2.plot(yearPa, pressure, 'b')
y2.set_ylabel('pressure [MPa]')
fig5.legend(labels = ('extraction rate', 'pressure'), loc=4,bbox_to_anchor=(1,1),bbox_transform=y1.transAxes)
plt.xlabel('year')
plt.title('comparison of pressure and extraction rate')
plt.tight_layout()

#show the plot to the screen OR save the plot in the directory
save_figure = False
if not save_figure:
	#Open a new window and display the plot
	plt.show()
else:
	#Save that plot to a png file
	plt.savefig('extraction vs pressure.png',dpi=300)





#pressure vs conc & extraction vs pressure
yearPa = np.arange(1980,2018,2)
yearCu=[1980,1985,1990,1995,2000,2005,2010,2015]
yearExtr = np.arange(1980, 2019)
fig5, (y1, y3) = plt.subplots(1, 2)
y1.plot(yearCu, dissolved_Cu, 'ko')
y1.set_ylabel('dissolved Cu [mg/litre]')
y2 = y1.twinx()
y2.plot(yearPa, pressure, 'r')
y2.set_ylabel('pressure [MPa]')
plt.title('comparison of pressure and Cu concentration')
plt.tight_layout()

y3.plot(yearPa, pressure, 'r')
y3.set_ylabel('dissolved Cu [mg/litre]')
y4 = y3.twinx()
y4.plot(yearExtr, extraction, 'b')
y4.set_ylabel('extraction [$10^6$ litre/day]')
fig5.legend(labels = ('Cu concentration', 'pressure', 'pressure', 'extraction rate' ), loc=4,bbox_to_anchor=(1,0.05),bbox_transform=y1.transAxes)
plt.title('comparison of extraction rate and Cu concentration')
plt.xlabel('year')

save_figure = False
if not save_figure:
	#Open a new window and display the plot
	plt.show()
else:
	#Save that plot to a png file
	plt.savefig('pressure_vs_conc & extraction_vs_conc.png',dpi=300)

