#Wegmans_Main.py

#DESCRPTIONS: 
	#this script is used for collecting online food data from Wegmans.

#INPUTS:
	

#VARIABLES:
	#WegmansDict:
		#Type: dict
		#Content: Information of all the Wegmans Stores
	
#FUNCTIONS:
	#WegmansStoreInfGet():
		#Source: WegmansStoreInf.py
		#Usage: Collect data of all the Wegmans Stores in NYS

#OUTPUTS:

#CREDITS:
	#Chengxi Zhu
	#Department of Geography
	#University at Buffalo, the State University of New York
	#Aug 2015
from WegmansStoreInf import *
import time
start_time = time.time()
WegmansDict=WegmansStoreInfGet()
print("--- %s seconds ---" % (time.time() - start_time))
print(WegmansDict)

