#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import glob, os.path, sys, re
#from geopy.geocoders import Bing
#from geopy import exc
import geocoder

PATH_DATA = 'data'

def main():
    np_concat = np.vectorize(concat)    

    # Tratamos los ficheros de Autonomos
    #for file in glob.glob(PATH_DATA + '/Autonomos*.csv'):
    #print('Parsing file %s' % file)
    frame = pd.read_csv('empresas_asturias/Empresas1(Asturias).csv', sep=';')
    frame['latitude'] = np.nan
    frame['longitude'] = np.nan
    frame['approximation'] = np.nan
    frame['concatenated'] = np_concat(frame['Direccion'], frame['CP'], frame['Poblacion'], frame['Provincia'], frame['Comunidad Autonoma'], 'España')
    #for i in range(0,100):
    for idx, row in frame.iterrows():
    	#address = frame.ix[i, 'concatenated']
    	address = row['concatenated']
    	#print address
    	###############################################################################
    	#						Codigo geopy										  #
    	###############################################################################
    	#geolocator = Bing()
    	#exception = False
    	#try:
    	#	location = geolocator.geocode(address, exactly_one=True, timeout=20)
    	#except geopy.exc.GeocoderTimedOut:
    	#	exception = True
    	#except geopy.exc.GeocoderQueryError:
    	#	exception = True
    	#print location.address
    	#print location.latitude
    	#print location.longitude
    	#print ""
    	#frame.loc[i, 'latitude'] = location.latitude if exception == False and location.latitude else np.nan
    	#frame.loc[i, 'longitude'] = location.longitude if exception == False and location.longitude else np.nan
    	###############################################################################
    	#						Codigo geocoder										  #
    	###############################################################################
    	location = geocoder.bing(address)
    	#print location.address
    	#print location.lat
    	#print location.lng
    	#print ""
    	#frame.loc[i, 'latitude'] = str(location.lat).replace(".",",") if location and location.lat else str(np.nan)
        #frame.loc[i, 'longitude'] = str(location.lng).replace(".",",") if location and location.lng else str(np.nan)
        #if location:
        #	if location.status != "OK":
        #		frame.loc[i, 'approximation'] = "2"
        #	elif str(frame.loc[i, 'Direccion']) == "nan":
        #		frame.loc[i, 'approximation'] = "2"
        #	else:
        #		frame.loc[i, 'approximation'] = "1"
        #else:
        #	frame.loc[i, 'approximation'] = np.nan
        frame.loc[idx, 'latitude'] = str(location.lat).replace(".",",") if location and location.lat else str(np.nan)
    	frame.loc[idx, 'longitude'] = str(location.lng).replace(".",",") if location and location.lng else str(np.nan)
        if location:
        	if location.status != "OK":
        		frame.loc[idx, 'approximation'] = "3"
        	elif str(frame.loc[idx, 'Direccion']) == "nan":
        		frame.loc[idx, 'approximation'] = "2"
        	else:
        		frame.loc[idx, 'approximation'] = "1"
        else:
        	frame.loc[idx, 'approximation'] = np.nan
    frame.__delitem__('concatenated')
    frame.to_csv('data_results.csv', sep=';')
    
        
def concat(*args):
    strs = [str(arg) for arg in args if not pd.isnull(arg)]
    strs[0] = strs[0].replace(","," ")
    strs[0] = strs[0].replace("."," ")
    subchain1 = re.findall("\([^\)]*\)",strs[0])
    strs[0] = strs[0] if len(subchain1) == 0 else strs[0].replace(subchain1[0], "")
    subchain2 = re.findall("[^0-9]+[0-9]{,3}",strs[0])
    strs[0] = strs[0] if len(subchain2) == 0 else subchain2[0]
    strs[2] = strs[2].replace("(",",")
    strs[2] = strs[2].replace(")","")
    return ','.join(strs) if strs else np.nan

def progress(current,total, text):
    sys.stdout.write('\r%s: %d/%d' % (text, current, total))
    sys.stdout.flush()

if __name__ == "__main__":
    main()

