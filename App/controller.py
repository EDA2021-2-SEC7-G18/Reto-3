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
from DISClib.Algorithms.Sorting import quicksort as qck
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
def loadAll(catalog):
    loadSightnings(catalog)
    loadCityIndex(catalog)
#Req 1
def calldatecmp(date1,date2):
    if date1 != '' and date2 != '':
        condition = model.datecmp(date1,date2)
    else:
        condition = False
    return condition
#Req 2

#Req 3

#Req 4

#Req 5

# Funciones de ordenamiento
def quicksort(catalog,cmpfunction):
    return qck.sort(catalog,cmpfunction)
# Funciones de consulta sobre el catálogo
