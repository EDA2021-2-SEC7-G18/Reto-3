"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import orderedmap as om
from prettytable import PrettyTable
from datetime import datetime, time
assert cf
import time

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Contar los avistamientos en una ciudad")
    print("3- Contar los avistamientos por duracion")
    print("4- Contar avistamientos por Hora/Minutos del dia")
    print("5- Contar los avistamientos en un rango de fechas")
    print("6- Contas los avistamientos de una Zona Geografica")

catalog = None
def initCatalog():
    return controller.init()

def loadAll(catalog):
    return controller.loadAll(catalog)
"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        start_time=time.time()
        print("Cargando información de los archivos ....")
        catalog=initCatalog()
        loadAll(catalog)
        print("--- %s seconds ---" % (time.time() - start_time))

    elif int(inputs[0]) == 2:
        city=str(input('Enter the city you want to consult'))
        start_time=time.time()
        datecmp =controller.calldatecmp
        size, citykeys, totalsize, dateIndex, dateIndexkeys= controller.KeysandSizes(catalog, city)
        max,maxcity= controller.mostsight(catalog, citykeys)
        numberofsightnings = 0
        newtable = controller.Construct_Max_Table(max, maxcity)
        maintable, numberofsightnings = controller.Construct_Cities_Tables(dateIndexkeys,dateIndex)
        print('There are ', totalsize, 'different cities with UFO sightings')
        print('The city with most UFO sightings is: ')
        print(newtable)
        print('There are',size,'sightnings at the ', city, 'city')
        print('the first and last 3 UFO sightnings in the city are:')
        print(maintable.get_string(start=0, end=3))
        if numberofsightnings >3:
            if numberofsightnings <6:
                print(maintable.get_string(start=(numberofsightnings)-(numberofsightnings%3), end=numberofsightnings))
            else:
                print(maintable.get_string(start=(numberofsightnings)-3, end=numberofsightnings))
        print("--- %s seconds ---" % (time.time() - start_time))

    elif int(inputs[0]) == 3:
        print('Altura del arbol de ciudades',om.height(catalog['cityIndex']))
        print('Numero de elementos (ciudades)',om.size(catalog['cityIndex']))

    elif int(inputs[0]) == 4:
        starttime= str(input('Ingrese la hora inicial '))
        starttime=datetime.strptime(starttime, '%H:%M')
        endtime= str(input('Ingrese la hora final '))
        endtime=datetime.strptime(endtime, '%H:%M')
        start_time=time.time()
        numberofsightnings=0
        keys=om.keySet(catalog['timeIndex'])
        cmp=controller.callrangetimecmp
        rangekeys=controller.callrangetime(keys,starttime,endtime, cmp)
        oldestdate = om.maxKey(catalog['timeIndex'])
        entry = om.get(catalog['timeIndex'], oldestdate)
        oldest = me.getValue(entry)
        oldkeys= om.keySet(oldest)
        oldestsize=0
        for i in lt.iterator(oldkeys):
            entry=om.get(oldest, i)
            value=me.getValue(entry)
            oldestsize+= lt.size(value)
        totalsize=om.size(catalog['timeIndex'])
        oldtable=PrettyTable()
        oldtable.field_names = ['date', 'count']
        oldtable.align='l'
        oldtable._max_width= {'date': 15,'count':15}
        oldtable.add_row([str(oldestdate),str(oldestsize)])
        maintable=PrettyTable()
        maintable.field_names = ['datetime','time','city','state','country','shape', 'duration (seconds)']
        maintable.align='l'
        maintable._max_width= {'datetime': 20,'time':20,'city':20,'state':20,'country':20,'shape':20, 'duration (seconds)':20}
        for item in lt.iterator(rangekeys):
            entry = om.get(catalog['timeIndex'], item)
            sightning = me.getValue(entry)
            sightningkeys=om.keySet(sightning)
            for element in lt.iterator(sightningkeys):
                entry=om.get(sightning,element)
                value=me.getValue(entry)
                for i in lt.iterator(value):
                    numberofsightnings+=1
                    shape = i['shape']
                    if shape == '':
                        shape = 'Unknown'
                    maintable.add_row([str(element), str(item),str(i['city']), str(i['state']), str(i['country']), shape ,str(i['duration (seconds)'])])
        print('There are ', totalsize, ' sightnings between:', starttime,'and',endtime)
        print('The latest UFO sightning time is: ')
        print(oldtable)
        print('\nThere are',numberofsightnings,' sightnings between', starttime, 'and', endtime, '\n')
        print('the first and last 3 UFO sightnings in this time are:')
        print(maintable.get_string(start=0, end=3))
        if numberofsightnings >3:
            if numberofsightnings <6:
                print(maintable.get_string(start=(numberofsightnings)-(numberofsightnings%3), end=numberofsightnings))
            else:
                print(maintable.get_string(start=(numberofsightnings)-3, end=numberofsightnings))
        print("--- %s seconds ---" % (time.time() - start_time))

    elif int(inputs[0]) == 5:
        startdate=str(input('Ingrese la fecha inicial '))
        startdate=datetime.strptime(startdate,'%Y-%m-%d')
        enddate=str(input('Ingrese la fecha final '))
        enddate=datetime.strptime(enddate,'%Y-%m-%d')
        start_time=time.time()
        keys = om.keySet(catalog['dateIndex'])
        cmp = controller.callrangecmp
        rangekeys = controller.callrangekeys(keys,catalog,startdate,enddate,cmp)
        oldtable = controller.Construct_Oldest_Table(catalog)
        maintable, numberofsightnings = controller.Construct_Dates_Table(catalog,rangekeys)
        difsight=om.size(catalog['dateIndex'])
        print('\nThere are',difsight,'UFO sightnings with different dates [YYYY-MM-DD]..')
        print('The oldest UFO sightnings date is:')
        print(oldtable)
        print('\nThere are',numberofsightnings,' sightnings between', startdate, 'and', enddate, '\n')
        print('the first and last 3 UFO sightnings in this time are:')
        print(maintable.get_string(start=0, end=3))
        if numberofsightnings >3:
            if numberofsightnings <6:
                print(maintable.get_string(start=(numberofsightnings)-(numberofsightnings%3), end=numberofsightnings))
            else:
                print(maintable.get_string(start=(numberofsightnings)-3, end=numberofsightnings))
        print("--- %s seconds ---" % (time.time() - start_time))

    elif int(inputs[0]) == 6:
        minlat=float(input('Ingrese la latitud minima'))
        minlat = round(minlat, 2)
        maxlat=float(input('Ingrese la latitud maxima'))
        maxlat = round(maxlat,2)
        minlong=float(input('Ingrese la longitud minima'))
        minlong = round(minlong, 2)
        maxlong = float(input('Ingrese la longitud maxima'))
        maxlong = round(maxlong, 2)
        start_time=time.time()
        keys=om.keySet(catalog['latitudeIndex'])
        latcmp=controller.callLatitudecmp
        pairs=controller.callrangelongitude(keys, catalog,minlong,maxlong, minlat,maxlat,latcmp)
        longitudecmp = controller.longitudecmp
        maintable, numberofsightnings = controller.Construct_Longitude_Table(catalog, pairs)
        print('There are',numberofsightnings,' sightnings between longitude: ', minlong, 'and', maxlong, ' and latitude: ', minlat, 'and', maxlat, '\n')
        print('the first and last 5 UFO sightnings in this area are:')
        print(maintable.get_string(start=0, end=5))
        if numberofsightnings>5:
            if numberofsightnings<10:
                print(maintable.get_string(start=(numberofsightnings)-(numberofsightnings%5), end=numberofsightnings))
            else:
                print(maintable.get_string(start=(numberofsightnings)-5, end=numberofsightnings))
        print("--- %s seconds ---" % (time.time() - start_time))
    else:
        sys.exit(0)
sys.exit(0)
