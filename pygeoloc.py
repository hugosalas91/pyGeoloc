#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import glob, os.path, geocoder, sys

PATH_DATA = 'data'

def main():
    np_concat = np.vectorize(concat)    

    # Tratamos los ficheros de Autonomos
    for file in glob.glob(PATH_DATA + '/Autonomos*.csv'):
        print('Parsing file %s' % file)
        frame = pd.read_csv(os.path.join(file))
        frame['latitude'] = np.nan
        frame['longitude'] = np.nan
        frame['concatenated'] = np_concat(frame['Direccion'], frame['Poblacion'], frame['PROVINCIA'])
        for idx, row in frame.iterrows():
	    progress(idx+1,len(frame)-1, 'Parsing row: ')
            address = row['concatenated']
            location = geocoder.google(address)
            row['latitude'] = location.lat if location and location.lat else np.nan
            row['longitude'] = location.lng if location and location.lng else np.nan
        frame.__delitem__('concatenated')
        name = '%s_parsed' % file
        frame.to_csv(name)
	print()
        
def concat(*args):
    strs = [str(arg) for arg in args if not pd.isnull(arg)]
    return ','.join(strs) if strs else np.nan

def progress(current,total, text):
    sys.stdout.write('\r%s: %d/%d' % (text, current, total))
    sys.stdout.flush()

if __name__ == "__main__":
    main()

# import codecs
# import json
# 
# # For Python 3.0 and later
# # from urllib.request import urlopen
# 
# f = open("Empresas1.csv", "r", encoding="utf-8")
# g = open("NuevoEmpresas1.csv","w")
# 
# #for linea in f:
# for i in range(1,4):
#     linea = f.readline()
#     elementosLinea = linea.split(';')
#     lugar = elementosLinea[4] + ', ' + elementosLinea[5] + ', ' + elementosLinea[6] + ', ' + elementosLinea[7] + ', ' + elementosLinea[8]
#     url = 'https://maps.googleapis.com/maps/api/geocode/json?address='
#     url += lugar.replace(' ','+') + '&sensor=false'
#     print(url)
#     response = urlopen(url)
#     reader = codecs.getreader("utf-8")
#     ret = json.load(reader(response))
#     if ret['results']:
#         #Me quedo únicamente con el primer resultado
#         latitud = ret['results'][0]['geometry']['location']['lat']
#         longitud = ret['results'][0]['geometry']['location']['lng']
#         g.write(elementosLinea[0])
#         g.write(";")
#         g.write(elementosLinea[1])
#         g.write(";")
#         g.write(elementosLinea[2])
#         g.write(";")
#         g.write(elementosLinea[3])
#         g.write(";")
#         g.write(elementosLinea[4])
#         g.write(";")
#         g.write(elementosLinea[5])
#         g.write(";")
#         g.write(elementosLinea[6])
#         g.write(";")
#         g.write(elementosLinea[7])
#         g.write(";")
#         g.write(elementosLinea[8])
#         g.write(";")
#         g.write(elementosLinea[9])
#         g.write(";")
#         g.write(str(latitud))
#         g.write(";")
#         g.write(str(longitud))
#         g.write(";")
#         g.write("\n")
# 
# f.close()
# g.close()
