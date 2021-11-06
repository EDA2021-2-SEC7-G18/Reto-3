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
 """

import config as cf
import model
import csv
from datetime import datetime
from DISClib.Algorithms.Sorting import mergesort as mrg
from DISClib.ADT import list as lt

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""
# Inicialización del Catálogo de libros
def init():
    catalog = model.newCatalog()
    return catalog
# Funciones para la carga de datos
def loadSightnings(catalog):
    UFOSfile = cf.data_dir + 'UFOS-utf8-small.csv'
    input_file = csv.DictReader(open(UFOSfile, encoding="utf-8"),
                                delimiter=",")
    for sightning in input_file:
        model.addSightning(catalog, sightning)
def loadCityIndex(catalog):
    for sightning in lt.iterator(catalog['sightnings']):
        model.updateCityIndex(catalog,sightning)
def loadDateIndex(catalog):
    for sightning in lt.iterator(catalog['sightnings']):
        model.updateDateIndex(catalog, sightning)
def loadLatitudeIndex(catalog):
    for sightning in lt.iterator(catalog['sightnings']):
        model.updateLatitude(catalog, sightning)
def loadtimeIndex(catalog):
    for sightning in lt.iterator(catalog['sightnings']):
        model.addtime(catalog, sightning)
def loadDurationIndex(catalog):
    for sightning in lt.iterator(catalog['sightnings']):
        model.loadDurationIndex(catalog, sightning)

def loadAll(catalog):
    loadSightnings(catalog)
    loadCityIndex(catalog)
    loadDateIndex(catalog)
    loadLatitudeIndex(catalog)
    loadtimeIndex(catalog)
    loadDurationIndex(catalog)
#Req 1
def calldatecmp(date1,date2):
    if date1 != '' and date2 != '':
        condition = model.datecmp(date1,date2)
    else:
        condition = False
    return condition
def mostsight(catalog,keys):
    return model.mostsight(catalog,keys)
def KeysandSizes(catalog, city):
    return model.KeysandSizes(catalog, city)
def Construct_Cities_Tables(dateIndexkeys,dateIndex):
    return model.Construct_Cities_Tables(dateIndexkeys,dateIndex)
def Construct_Max_Table(max, maxcity):
    return model. Construct_Max_Table(max, maxcity)
#Req 2
def getmax(catalog):
    return model.getmax(catalog)

def getinterval(catalog, low, high):
    return model.getinterval(catalog, low, high)

def getfirstlast(interval):
    primeros = []
    ultimos = []
    lista = lt.newList('ARRAY_LIST')
    for duration in lt.iterator(interval):
        for elemento in lt.iterator(duration):
            lt.addLast(lista, elemento)
    for i in range(1,4):
        complete = lt.getElement(lista, i)
        elemento = [i, complete['datetime'], complete['city'], complete['country'], complete['shape'], complete['duration (seconds)']]
        primeros.append(elemento)
        
    for i in range(lt.size(lista)-2,lt.size(lista) + 1):
        complete = lt.getElement(lista, i)
        elemento = [i, complete['datetime'], complete['city'], complete['country'], complete['shape'], complete['duration (seconds)']]
        ultimos.append(elemento)

    return primeros, ultimos
#Req 3
def callsorttimecmp(date1,date2):
    if date1 != '' and date2 !='':
        condition=model.sorttimecmp
    else:
        condition =False
    return condition
def callrangetime(keys,start,end, cmp):
    if keys != None:
        condition = model.rangetime(keys,start,end,cmp)
    else:
        condition = 'No sightnings found in range'
    return condition

def callrangetimecmp(time, start,end):
    if time!='':
        condition=model.rangetimecmp(time,start,end)
    else:
        condition=False
    return condition
#Req 4
def callsimpledatecmp(date1,date2):
    if date1 != '' and date2 != '':
        condition = model.simpledatecmp(date1,date2)
    else:
        condition = False
    return condition
def callrangecmp(date, start,end):
    if date != '':
        condition =model.rangecmp(date, start, end)
    else:
        condition = False
    return condition
def callrangekeys(keys,catalog,start,end, cmp):
    if keys != None:
        condition = model.rangekeys(keys,catalog,start,end,cmp)
    else:
        condition = 'No sightnings found in range'
    return condition
def Construct_Oldest_Table(catalog):
    return model.Construct_Oldest_Table(catalog)
def Construct_Dates_Table(catalog, rangekeys):
    return model.Construct_Dates_Table(catalog, rangekeys)
#Req 5
def callsortlongitude(long1,long2):
    if long1 != '' and long2 != '':
        condition=model.sortlongitude
    else:
        condition=False
    return condition
def callLatitudecmp(longitude, minimum, maximum):
    if type(longitude) != str:
        condition = model.latitudecmp(longitude, minimum, maximum)
    else:
        condition=False
    return condition
def longitudecmp(lat1,lat2):
    if lat1 !='' and lat2 != '':
        condition = model.longitudecmp(abs(float(lat1['latitude'])), abs(float(lat1['latitude'])))
    else:
        condition = False
    return condition
def callrangelongitude(keys, catalog,minlong,maxlong,minlat,maxlat, cmp):
    if keys != None:
        condition = model.rangelongitude(keys,catalog,minlong,maxlong,minlat,maxlat,cmp)
    else:
        condition = 'No sightnings found in range'
    return condition
def Construct_Longitude_Table(catalog, pairs):
    return model.Construct_Longitude_Table(catalog, pairs)
# Funciones de ordenamiento
def mergesort(catalog, cmp):
    return mrg.sort(catalog, cmp)
# Funciones de consulta sobre el catálogo
