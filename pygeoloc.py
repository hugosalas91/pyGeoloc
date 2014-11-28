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
	    progress(idx,len(frame), 'Parsing row: ')
            address = row['concatenated']
            location = geocoder.bing(address)
            frame.loc[idx, 'latitude'] = location.lat if location and location.lat else np.nan
            frame.loc[idx, 'longitude'] = location.lng if location and location.lng else np.nan
        frame.__delitem__('concatenated')
        name = '%s_parsed' % file
        frame.to_csv(name)
        
def concat(*args):
    strs = [str(arg) for arg in args if not pd.isnull(arg)]
    return ','.join(strs) if strs else np.nan

def progress(current,total, text):
    sys.stdout.write('\r%s: %d/%d' % (text, current, total))
    sys.stdout.flush()

if __name__ == "__main__":
    main()
