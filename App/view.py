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
from datetime import datetime
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
        pass
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
        maintable=PrettyTable()
        maintable.field_names = ['datetime','city','state','country','shape', 'duration (seconds)']
        maintable.align='l'
        maintable._max_width= {'datetime': 20,'city':20,'state':20,'country':20,'shape':20, 'duration (seconds)':20}
        oldestdate = lt.firstElement(sortedkeys)
        entry = om.get(catalog['dateIndex'], oldestdate)
        oldest = me.getValue(entry)
        oldestsize= lt.size(oldest)
        for item in lt.iterator(sortedkeys):
            entry = om.get(catalog['dateIndex'], item)
            sightning = me.getValue(entry)
            for element in lt.iterator(sightning):
                shape = element['shape']
                if shape == '':
                    shape = 'Unknown'
                maintable.add_row([str(element['datetime']), str(element['city']), str(element['state']), str(element['country']), shape ,str(element['duration (seconds)'])])
        print('The number of sightnings with the oldest date is ' , oldestsize)
        print('There are',numberofsightnings,' sightnings between', startdate, 'and', enddate, '\n')
        print('the first and last 3 UFO sightnings in this time are:')
        print(maintable.get_string(start=0, end=3))
        print(maintable.get_string(start=(numberofsightnings)-3, end=numberofsightnings))
        
    elif int(inputs[0]) == 6:
        pass
    else:
        sys.exit(0)
sys.exit(0)
