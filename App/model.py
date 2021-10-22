"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from datetime import datetime
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def newCatalog():
    catalog = {'sightnings': None,
    'dateIndex': None}
    catalog = ['sightnings'] = lt.newList('ARRAY_LIST', cmpfunction=None)
    catalog['cityIndex'] = mp.newMap(omaptype ='BST', comparefunction=compareDates)
    return catalog

# Funciones para agregar informacion al catalogo
def newDataEntry(sightning):
    entry = {''}
def updateDateIndex(map, sightning):
    city=sightning['city']
    entry = om.get(map, city)
    if entry is None:
        cityentry = newDataEntry(sightning)
        om.put(map, city, cityentry)
    else:
        cityentry = me.getValue(entry)
    addDateIndex(cityentry, sightning)
    return map

def addCrime(catalog, sightning):
    lt.addLast(catalog['sightning'], sightning)
    updateDateIndex(catalog['dateIndex'], sightning) 
# Funciones para creacion de datos

#Req 1

#Req 2

#Req 3

#Req 4

#Req 5

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista
def compareIds(id1, id2):
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1
def compareDates(date1,date2):
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return-1
# Funciones de ordenamiento
