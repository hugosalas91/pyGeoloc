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
    frame = pd.read_csv('Empresas1.csv', sep=';')
    frame['latitude'] = np.nan
    frame['longitude'] = np.nan
    frame['concatenated'] = np_concat(frame['Direccion'], frame['CP'], frame['Poblacion'], frame['Provincia'], frame['Comunidad Autonoma'], 'España')
    for i in range(0,60):
    	address = frame.ix[i, 'concatenated']
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
    	location = geocoder.google(address)
    	#print location.address
    	#print location.lat
    	#print location.lng
    	#print ""
    	frame.loc[i, 'latitude'] = location.lat if location and location.lat else np.nan
        frame.loc[i, 'longitude'] = location.lng if location and location.lng else np.nan
    frame.__delitem__('concatenated')
    name = '%s_parsed' % file
    frame.to_csv(name)
    
    #for idx, row in frame.iterrows():
    #    progress(idx,len(frame), 'Parsing row: ')
    #    address = row['concatenated']
    #    location = geocoder.bing(address)
    #    frame.loc[idx, 'latitude'] = location.lat if location and location.lat else np.nan
    #    frame.loc[idx, 'longitude'] = location.lng if location and location.lng else np.nan
    #frame.__delitem__('concatenated')
    #name = '%s_parsed' % file
    #frame.to_csv(name)
        
def concat(*args):
    strs = [str(arg) for arg in args if not pd.isnull(arg)]
    strs[0] = strs[0].replace(","," ")
    subchain = re.findall("[^0-9]+[0-9]{,3}",strs[0])
    strs[0] = strs[0] if len(subchain) == 0 else subchain[0]
    return ','.join(strs) if strs else np.nan

def progress(current,total, text):
    sys.stdout.write('\r%s: %d/%d' % (text, current, total))
    sys.stdout.flush()

if __name__ == "__main__":
    main()