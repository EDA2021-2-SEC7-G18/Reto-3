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


from typing import OrderedDict
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
    catalog = {'cityIndex': None, 'sightnings':None, 'dateIndex':None, 'longitudeIndex':None}
    catalog['cityIndex'] = om.newMap(omaptype='RBT', comparefunction=compareCities)
    catalog['sightnings'] = lt.newList('ARRAY_LIST',cmpfunction=None)
    catalog['dateIndex']= om.newMap(omaptype='RBT', comparefunction=compareDates)
    catalog['longitudeIndex'] = om.newMap(omaptype='RBT', comparefunction=compareLongitude)
    return catalog

# Funciones para agregar informacion al catalogo
def addSightning(catalog, sightning):
    lt.addLast(catalog['sightnings'], sightning)
def addDate(dateIndex, sightning):
    date=sightning['datetime']
    entry = om.get(dateIndex, date)
    if entry is None:
        Data= lt.newList('ARRAY_LIST', cmpfunction=None)
        om.put(dateIndex, date, Data)
    else:
        Data = me.getValue(entry)
    lt.addLast(Data, sightning)

def updateDateIndex(catalog, sightning):
    date=datetime.strptime(sightning['datetime'], '%Y-%m-%d %H:%M:%S')
    reconstructdate = str(date.year) + '-' + str(date.month) + '-' + str(date.day)
    entry = om.get(catalog['dateIndex'], reconstructdate)
    if entry is None:
        datelist = lt.newList('ARRAY_LIST', cmpfunction=None)
        om.put(catalog['dateIndex'], reconstructdate , datelist)
    else:
        datelist = me.getValue(entry)
    lt.addLast(datelist, sightning)

def updateCityIndex(catalog, sightning):
    city=sightning['city']
    entry = om.get(catalog['cityIndex'], city)
    if entry is None:
        dateIndex = om.newMap(omaptype='RBT', comparefunction=comparefullDates)
        om.put(catalog['cityIndex'], city, dateIndex)
    else:
        dateIndex = me.getValue(entry)
    addDate(dateIndex, sightning)

def addLatitude(latitudeIndex, sightning):
    latitude=sightning['latitude']
    entry = om.get(latitudeIndex, latitude)
    if entry is None:
        Data= lt.newList('ARRAY_LIST', cmpfunction=None)
        om.put(latitudeIndex, latitude, Data)
    else:
        Data = me.getValue(entry)
    lt.addLast(Data, sightning)

def updateLongitude(catalog, sightning):
    longitude= sightning['longitude']
    entry = om.get(catalog['longitudeIndex'], longitude)
    if entry is None:
        latitudeIndex = om.newMap(omaptype='RBT', comparefunction=compareLongitude)
        om.put(catalog['longitudeIndex'], longitude, latitudeIndex)
    else:
        latitudeIndex = me.getValue(entry)
    addLatitude(latitudeIndex, sightning)
# Funciones para creacion de datos

#Req 1
def datecmp(date1, date2):
    return datetime.strptime(date1, '%Y-%m-%d %H:%M:%S') < datetime.strptime(date2,'%Y-%m-%d %H:%M:%S')
#Req 2

#Req 3

#Req 4
def simpledatecmp(date1, date2):
    return datetime.strptime(date1, '%Y-%m-%d') < datetime.strptime(date2,'%Y-%m-%d')
def rangecmp(date, start, end):
    return (datetime.strptime(date,'%Y-%m-%d') > start) and (datetime.strptime(date,'%Y-%m-%d') < end)
def rangekeys(keys,catalog,start, end, cmp):
    numerosightnings = 0
    lst = lt.newList('ARRAY_LIST')
    for item in lt.iterator(keys):
        if cmp(item, start,end):
            entry = om.get(catalog['dateIndex'], item)
            sightning = me.getValue(entry)
            numerosightnings += lt.size(sightning)
            lt.addLast(lst, item)
    return lst, numerosightnings

#Req 5
def sortlongitude(long1,long2):
    lat1=long1['latitude']
    lat2=long2['latitude']
    modlongitude1 = round(float(lat1), 2)
    modlongitude2 = round(float(lat2), 2)
    return abs(modlongitude1) < abs(modlongitude2)
def longitudecmp(longitude, minimum, maximum):
    modlongitude = round(float(longitude), 2)
    return (abs(modlongitude)>abs(minimum)) and (abs(modlongitude)<abs(maximum))
def rangelongitude(keys, catalog,minlong,maxlong,minlat,maxlat,cmp):
    list=lt.newList('ARRAY_LIST', cmpfunction=None)
    numbersightnings =0
    for item in lt.iterator(keys):
        dictionary = OrderedDict()
        if item != '':
            if cmp(float(item), minlong,maxlong,):
                entry = om.get(catalog['longitudeIndex'], item)
                sightning = me.getValue(entry)
                latkeys= om.keySet(sightning)
                dictionary['longitude']=item
                for latitude in lt.iterator(latkeys):
                    if latitude != '':
                        if cmp(float(latitude), minlat,maxlat):
                            dictionary['latitude']=latitude
                            lt.addLast(list, dictionary)
                            numbersightnings += 1
    return list, numbersightnings

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista
def compareCities(id1, id2):
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1
def compareLongitude(long1,long2):
    if (long1 == long2):
        return 0
    elif long1 > long2:
        return 1
    else:
        return -1
def comparefullDates(date1,date2):
    date11=datetime.strptime(date1, '%Y-%m-%d %H:%M:%S')
    date22=datetime.strptime(date2, '%Y-%m-%d %H:%M:%S')
    if (date11 == date22):
        return 0
    elif (date11 > date22):
        return 1
    else:
        return-1
def compareDates(date1,date2):
    date11=datetime.strptime(date1, '%Y-%m-%d')
    date22=datetime.strptime(date2, '%Y-%m-%d')
    if (date11 == date22):
        return 0
    elif (date11 > date22):
        return 1
    else:
        return-1
# Funciones de ordenamiento