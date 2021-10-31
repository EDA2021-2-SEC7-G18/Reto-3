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
        print("Cargando información de los archivos ....")
        catalog=initCatalog()
        loadAll(catalog)
    elif int(inputs[0]) == 2:
        city=str(input('Enter the city you want to consult'))
        datecmp =controller.calldatecmp
        entry = om.get(catalog['cityIndex'], city)
        dateIndex = me.getValue(entry)
        size=om.size(dateIndex)
        keys = om.keySet(dateIndex)
        numberofsightnings = om.size(dateIndex)
        sortedkeys=controller.quicksort(keys, datecmp)
        maintable=PrettyTable()
        maintable.field_names = ['datetime','city','state','country','shape', 'duration (seconds)']
        maintable.align='l'
        maintable._max_width= {'datetime': 20,'city':20,'state':20,'country':20,'shape':20, 'duration (seconds)':20}
        for item in lt.iterator(sortedkeys):
            entry = om.get(dateIndex, item)
            sightning = me.getValue(entry)
            for element in lt.iterator(sightning):
                shape = element['shape']
                if shape == '':
                    shape = 'Unknown'
                maintable.add_row([str(element['datetime']), str(element['city']), str(element['state']), str(element['country']), shape ,str(element['duration (seconds)'])])
        print('There are',size,'different cities with UFO sightnings')
        print('the first and last 3 UFO sightnings in the city are:')
        print(maintable.get_string(start=0, end=3))
        print(maintable.get_string(start=(numberofsightnings)-3, end=numberofsightnings))
    elif int(inputs[0]) == 3:
        print('Altura del arbol de ciudades',om.height(catalog['cityIndex']))
        print('Numero de elementos (ciudades)',om.size(catalog['cityIndex']))
    elif int(inputs[0]) == 4:
        starttime= str(input('Ingrese la hora inicial '))
        starttime=datetime.strptime(starttime, '%H:%M')
        starttime=str(starttime.hour)+':'+str(starttime.minute)
        endtime= str(input('Ingrese la hora final '))
        endtime=datetime.strptime(endtime, '%H:%M')
        endtime=str(endtime.hour)+':'+str(endtime.minute)
        keys=om.keySet(catalog['fulldateIndex'])
        cmp=controller.callrangetimecmp
        rangekeys,numberofsightnings=controller.callrangetime(keys,catalog,starttime,endtime, cmp)
        sortcmp=controller.callsorttimecmp
        sortedkeys=controller.quicksort(rangekeys, sortcmp)
        print(sortedkeys)
        oldestdate = om.maxKey(catalog['timeIndex'])
        entry = om.get(catalog['timeIndex'], oldestdate)
        oldest = me.getValue(entry)
        oldestsize= lt.size(oldest)
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
        for item in lt.iterator(sortedkeys):
            entry = om.get(catalog['fulldateIndex'], item)
            sightning = me.getValue(entry)
            for element in lt.iterator(sightning):
                date=datetime.strptime(element['datetime'], '%Y-%m-%d %H:%M:%S')
                fecha=str(date.year)+'-'+str(date.month)+'-'+str(date.day)
                hora=str(date.hour)+':'+str(date.minute)
                shape = element['shape']
                if shape == '':
                    shape = 'Unknown'
                maintable.add_row([str(fecha), str(hora),str(element['city']), str(element['state']), str(element['country']), shape ,str(element['duration (seconds)'])])
        print('There are ', totalsize, ' sightnings between:', starttime,'and',endtime)
        print('The latest UFO sightning time is: ')
        print(oldtable)
        print('\nThere are',numberofsightnings,' sightnings between', starttime, 'and', endtime, '\n')
        print('the first and last 3 UFO sightnings in this time are:')
        print(maintable.get_string(start=0, end=3))
        print(maintable.get_string(start=(numberofsightnings)-3, end=numberofsightnings))

    elif int(inputs[0]) == 5:
        startdate=str(input('Ingrese la fecha inicial '))
        startdate=datetime.strptime(startdate,'%Y-%m-%d')
        enddate=str(input('Ingrese la fecha final '))
        enddate=datetime.strptime(enddate,'%Y-%m-%d')
        keys = om.keySet(catalog['dateIndex'])
        cmp = controller.callrangecmp
        rangekeys,numberofsightnings = controller.callrangekeys(keys,catalog,startdate,enddate,cmp)
        sortcmp = controller.callsimpledatecmp
        sortedkeys = controller.shellsort(rangekeys, sortcmp)
        oldestdate = om.minKey(catalog['dateIndex'])
        entry = om.get(catalog['dateIndex'], oldestdate)
        oldest = me.getValue(entry)
        oldestsize= lt.size(oldest)
        oldtable=PrettyTable()
        oldtable.field_names = ['date', 'count']
        oldtable.align='l'
        oldtable._max_width= {'date': 15,'count':15}
        oldtable.add_row([str(oldestdate),oldestsize])
        maintable=PrettyTable()
        maintable.field_names = ['datetime','city','state','country','shape', 'duration (seconds)']
        maintable.align='l'
        maintable._max_width= {'datetime': 20,'city':20,'state':20,'country':20,'shape':20, 'duration (seconds)':20}
        for item in lt.iterator(sortedkeys):
            entry = om.get(catalog['dateIndex'], item)
            sightning = me.getValue(entry)
            for element in lt.iterator(sightning):
                shape = element['shape']
                if shape == '':
                    shape = 'Unknown'
                maintable.add_row([str(element['datetime']), str(element['city']), str(element['state']), str(element['country']), shape ,str(element['duration (seconds)'])])
        difsight=om.size(catalog['dateIndex'])
        print('\nThere are',difsight,'UFO sightnings with different dates [YYYY-MM-DD]..')
        print('The oldest UFO sightnings date is:')
        print(oldtable)
        print('\nThere are',numberofsightnings,' sightnings between', startdate, 'and', enddate, '\n')
        print('the first and last 3 UFO sightnings in this time are:')
        print(maintable.get_string(start=0, end=3))
        print(maintable.get_string(start=(numberofsightnings)-3, end=numberofsightnings))
        
    elif int(inputs[0]) == 6:
        minlong=float(input('Ingrese la longitud minima'))
        minlong = round(minlong, 2)
        maxlong = float(input('Ingrese la longitud maxima'))
        maxlong = round(maxlong, 2)
        minlat=float(input('Ingrese la latitud minima'))
        minlat = round(minlat, 2)
        maxlat=float(input('Ingrese la latitud maxima'))
        maxlat = round(maxlat,2)
        keys=om.keySet(catalog['longitudeIndex'])
        longcmp=controller.callLongitudecmp
        sortcmp=controller.callsortlongitude
        pairs,numberofsightnings=controller.callrangelongitude(keys, catalog,minlong,maxlong, minlat,maxlat,longcmp)
        sortedpairs=controller.quicksort(pairs,sortcmp)
        maintable=PrettyTable()
        maintable.field_names = ['datetime','city','state','country','shape', 'duration (seconds)', 'longitude', 'latitude']
        maintable.align='l'
        maintable._max_width= {'datetime': 20,'city':20,'state':20,'country':20,'shape':20, 'duration (seconds)':20,'longitude':20, 'latitude':20}
        for item in lt.iterator(pairs):
            entrylong = om.get(catalog['longitudeIndex'], item['longitude'])
            latmap = me.getValue(entrylong)
            entrylat = om.get(latmap, item['latitude'])
            sightnings = me.getValue(entrylat)
            for avistamiento in lt.iterator(sightnings):
                shape = avistamiento['shape']
                if shape == '':
                    shape = 'Unknown'
                maintable.add_row([str(avistamiento['datetime']), str(avistamiento['city']), str(avistamiento['state']), str(avistamiento['country']), shape ,str(avistamiento['duration (seconds)']), round(float(avistamiento['longitude']),2), round(float(avistamiento['latitude']),2)])
        print('There are',numberofsightnings,' sightnings between longitude: ', minlong, 'and', maxlong, ' and latitude: ', minlat, 'and', maxlat, '\n')
        print('the first and last 5 UFO sightnings in this area are:')
        print(maintable.get_string(start=0, end=5))
        if numberofsightnings>5:
            if numberofsightnings<10:
                print(maintable.get_string(start=(numberofsightnings)-(numberofsightnings%5), end=numberofsightnings))
            else:
                print(maintable.get_string(start=(numberofsightnings)-5, end=numberofsightnings))
    else:
        sys.exit(0)
sys.exit(0)
