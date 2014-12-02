pyGeoloc
========

Address Geolocalization for Python 2

Para mejorar los resultados de geolocalización se ha tenido que realizar un preprocesado minucioso de los datos de un archivo .xlxs, ya que estos eran de mala calidad. Se ha hecho lo siguiente:

- Tratar el .xlxs

Convertir:
Ñ - N
ñ - n
á - a
é - e
í - i
ó - o
ú - u
à - a
è - e
ì - i
ò - o
ù - u
Â· -
Ã‰ - e
Ã‘ - n
ÃŠ - u
Ã“ - o
Ã³ - o
Ã± - n
Ã¡ - a
Ãˆ - e
Ã - a
ä - a
ë - e
ï - i
ö - o
ü - u
Ç - c
¡ -
! -
¿ -
º -
ª -

Una vez cambiados estos caracteres conflictivos por los indicados se genera a partir del archivo .xlxs un .csv, y tratamos algunos caracteres conflictivos más que aún se nos han generado.

- Tratar el csv

Convertir:
á - 
aà - c
à - 
ò - 
â - 
ê - 
î - 
ô - 
û - 
ã - 
aÕ - o

Por último como vemos en el código tratamos un poco más los datos, para eliminar caracteres que aún nos pueden dar problemas, asi como trozos de cadenas en la dirección (piso, aclaraciones entre paréntesis, etc...).

- Tratar el código

En el campo dirección quitar las comas:
strs[0] = strs[0].replace(","," “)

En el campo dirección quitar los puntos:
strs[0] = strs[0].replace("."," ")

En el campo dirección quitar los textos entre paréntesis:
re.findall("\([^\)]*\)",strs[0])

En el campo dirección cortar la cadena después del número de portal:
re.findall("[^0-9]+[0-9]{,3}",strs[0])

En el campo Poblacion quitar paréntesis, sustituyendo el primero por una coma.
strs[2] = strs[2].replace("(",",")
strs[2] = strs[2].replace(")","")
