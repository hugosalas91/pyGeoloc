# coding: utf-8

import codecs
import json

# For Python 3.0 and later
from urllib.request import urlopen

f = open("Empresas1.csv", "r", encoding="utf-8")
g = open("NuevoEmpresas1.csv","w")

#for linea in f:
for i in range(1,4):
    linea = f.readline()
    elementosLinea = linea.split(';')
    lugar = elementosLinea[4] + ', ' + elementosLinea[5] + ', ' + elementosLinea[6] + ', ' + elementosLinea[7] + ', ' + elementosLinea[8]
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address='
    url += lugar.replace(' ','+') + '&sensor=false'
    print(url)
    response = urlopen(url)
    reader = codecs.getreader("utf-8")
    ret = json.load(reader(response))
    if ret['results']:
        #Me quedo únicamente con el primer resultado
        latitud = ret['results'][0]['geometry']['location']['lat']
        longitud = ret['results'][0]['geometry']['location']['lng']
        g.write(elementosLinea[0])
        g.write(";")
        g.write(elementosLinea[1])
        g.write(";")
        g.write(elementosLinea[2])
        g.write(";")
        g.write(elementosLinea[3])
        g.write(";")
        g.write(elementosLinea[4])
        g.write(";")
        g.write(elementosLinea[5])
        g.write(";")
        g.write(elementosLinea[6])
        g.write(";")
        g.write(elementosLinea[7])
        g.write(";")
        g.write(elementosLinea[8])
        g.write(";")
        g.write(elementosLinea[9])
        g.write(";")
        g.write(str(latitud))
        g.write(";")
        g.write(str(longitud))
        g.write(";")
        g.write("\n")

f.close()
g.close()
