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

from datetime import datetime
from prettytable import PrettyTable
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def newCatalog():
    catalog = {'cityIndex': None, 'sightnings':None, 'dateIndex':None, 'latitudeIndex':None, 'timeIndex':None}
    catalog['cityIndex'] = om.newMap(omaptype='RBT', comparefunction=compareCities)
    catalog['sightnings'] = lt.newList('ARRAY_LIST',cmpfunction=None)
    catalog['dateIndex']= om.newMap(omaptype='RBT', comparefunction=compareDates)
    catalog['latitudeIndex'] = om.newMap(omaptype='RBT', comparefunction=compareLongitude)
    catalog['timeIndex']=om.newMap(omaptype='RBT', comparefunction=comparetime)
    catalog['DurationIndex']=om.newMap(omaptype='RBT')#, comparefunction = compareDurations)
    catalog['Dtimes'] = om.newMap(omaptype ='RBT')
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

def addLongitude(longitudeIndex, sightning):
    longitude=sightning['longitude']
    entry = om.get(longitudeIndex, longitude)
    if entry is None:
        Data= lt.newList('ARRAY_LIST', cmpfunction=None)
        om.put(longitudeIndex, longitude, Data)
    else:
        Data = me.getValue(entry)
    lt.addLast(Data, sightning)
def addsubDate(timeIndex, sightning):
    date=sightning['datetime']
    entry = om.get(timeIndex, date)
    if entry is None:
        datelist = lt.newList('ARRAY_LIST', cmpfunction=None)
        om.put(timeIndex, date , datelist)
    else:
        datelist = me.getValue(entry)
    lt.addLast(datelist, sightning)

def addtime(catalog, sightning):
    tiempo=datetime.strptime(sightning['datetime'],'%Y-%m-%d %H:%M:%S')
    modtiempo=str(tiempo.hour)+':'+str(tiempo.minute)
    entry = om.get(catalog['timeIndex'], modtiempo)
    if entry is None:
        dateIndex = om.newMap(omaptype='RBT', comparefunction=comparefullDates)
        om.put(catalog['timeIndex'], modtiempo, dateIndex)
    else:
        dateIndex = me.getValue(entry)
    addDate(dateIndex, sightning)

def updateLatitude(catalog, sightning):
    latitude= sightning['latitude']
    entry = om.get(catalog['latitudeIndex'], latitude)
    if entry is None:
        longitudeIndex = om.newMap(omaptype='RBT', comparefunction=compareLongitude)
        om.put(catalog['latitudeIndex'], latitude, longitudeIndex)
    else:
        longitudeIndex = me.getValue(entry)
    addLongitude(longitudeIndex, sightning)

def loadDurationIndex(catalog, sightning):
    duration= float(sightning['duration (seconds)'])
    entry = om.get(catalog['DurationIndex'], duration)
    #key = sightning['country']
    if entry is None:
        DurationIndex = lt.newList('SINGLE_LINKED', cmpfunction= comparestrings)
        om.put(catalog['DurationIndex'], duration, DurationIndex)
    else:
        DurationIndex = me.getValue(entry)
        lt.addLast(DurationIndex, sightning)
    loadDtimes(catalog, duration)

def loadDtimes(catalog,duration):
    val = 1
    conditional = lt.isPresent(om.keySet(catalog['Dtimes']), duration)
    if conditional == 0:
        om.put(catalog['Dtimes'], duration, val)
    else:# conditional !=0:
        entry = om.get(catalog['Dtimes'], float(duration))
        val = me.getValue(entry) +1
        om.put(catalog['Dtimes'], float(duration), conditional)
# Funciones para creacion de datos

#Req 1
def Return_Values_and_Keys(catalog, variable, conditional):
    entry=om.get(catalog, variable)
    value=me.getValue(entry)
    newkeys=om.keySet(value)
    if conditional:
        result = value, newkeys
    else:
        result = newkeys
    return result
def Return_OM_Size(catalog, variable):
    entry=om.get(catalog, variable)
    value=me.getValue(entry)
    size = om.size(value)
    return size
def Return_List_Size(catalog, variable):
    entry=om.get(catalog, variable)
    value=me.getValue(entry)
    size = lt.size(value)
    return size
def datecmp(date1, date2):
    return datetime.strptime(date1['datetime'], '%Y-%m-%d %H:%M:%S') < datetime.strptime(date2['datetime'],'%Y-%m-%d %H:%M:%S')

def mostsight(catalog,keys):
    max=0
    maxcity=''
    for variable in lt.iterator(keys):
        counter = 0
        size= Return_List_Size(catalog['cityIndex'], variable)
        counter+=size
        if counter > max:
            max=counter
            maxcity= variable
    return max, maxcity
def mostsight1(catalog,keys):
    max=0
    maxcity=''
    for variable in lt.iterator(keys):
        size= Return_OM_Size(catalog['cityIndex'], variable)
        counter=size
        if counter > max:
            max=counter
            maxcity= variable
    return max, maxcity
def KeysandSizes(catalog, city):
    entry = om.get(catalog['cityIndex'], city)
    dateIndex = me.getValue(entry)
    size=lt.size(dateIndex)
    citykeys=om.keySet(catalog['cityIndex'])
    totalsize=om.size(catalog['cityIndex'])
    return size, citykeys, totalsize, dateIndex

def Construct_Cities_Tables(sorteddate):
    maintable=PrettyTable()
    maintable.field_names = ['datetime','city','state','country','shape', 'duration (seconds)']
    maintable.align='l'
    maintable._max_width= {'datetime': 20,'city':20,'state':20,'country':20,'shape':20, 'duration (seconds)':20}
    for element in lt.iterator(sorteddate):
        shape = element['shape']
        if shape == '':
            shape = 'Unknown'
        maintable.add_row([str(element['datetime']), str(element['city']), str(element['state']), str(element['country']), shape ,str(element['duration (seconds)'])])
    return maintable

def Construct_Max_Table(max, maxcity):
    newtable=PrettyTable()
    newtable.field_names = ['city','sightings']
    newtable.align='l'
    newtable._max_width= {'city':20,'sightings':20}
    newtable.add_row([str(maxcity), str(max)])
    return newtable

#Req 2
def rangetimecmp(time, start,end):
    modtime=datetime.strptime(time,'%H:%M')
    return (modtime>=start) and (modtime<=end)
def rangetime(catalog,keys,start, end, cmp):
    lst = lt.newList('ARRAY_LIST', cmpfunction=None)
    numberofsightnings=0
    for item in lt.iterator(keys):
        if cmp(item, start,end):
            entry = om.get(catalog['timeIndex'], item)
            value= me.getValue(entry)
            numberofsightnings+=lt.size(value)
            lt.addLast(lst, item)
    return lst, numberofsightnings
def timecmp(time1, time2):
    return datetime.strptime(time1['datetime'],'%Y-%m-%d %H:%M:%S')<datetime.strptime(time2['datetime'],'%Y-%m-%d %H:%M:%S')
def Construct_Oldest_Time_Table(catalog):
    oldestdate = om.maxKey(catalog['timeIndex'])
    entry = om.get(catalog['timeIndex'], oldestdate)
    oldest = me.getValue(entry)
    oldestsize=lt.size(oldest)
    oldtable=PrettyTable()
    oldtable.field_names = ['date', 'count']
    oldtable.align='l'
    oldtable._max_width= {'date': 15,'count':15}
    oldtable.add_row([str(oldestdate),str(oldestsize)])
    return oldtable
def Construct_Time_Table(catalog, rangekeys,cmp, numberofsightnings):
    maintable=PrettyTable()
    maintable.field_names = ['datetime','city','state','country','shape', 'duration (seconds)']
    maintable.align='l'
    maintable._max_width= {'datetime': 20,'city':20,'state':20,'country':20,'shape':20, 'duration (seconds)':20}
    counter = 0
    for item in lt.iterator(rangekeys):
        entry = om.get(catalog['timeIndex'], item)
        sightning = me.getValue(entry)
        sortedkeys = controller.mergesort(sightning, cmp)
        for element in lt.iterator(sortedkeys):
            shape = element['shape']
            if shape == '':
                shape = 'Unknown'
            maintable.add_row([str(element['datetime']), str(element['city']), str(element['state']), str(element['country']), shape ,str(element['duration (seconds)'])])
            counter +=1
            if counter >=3:
                break
    endtable=PrettyTable()
    endtable.field_names = ['datetime','city','state','country','shape', 'duration (seconds)']
    endtable.align='l'
    endtable._max_width= {'datetime': 20,'city':20,'state':20,'country':20,'shape':20, 'duration (seconds)':20}
    if  numberofsightnings> 3:
        endtablesize = 0
        sublst= lt.subList(rangekeys, lt.size(rangekeys)-2,3)
        for item in lt.iterator(sublst):
            entry = om.get(catalog['timeIndex'], item)
            sightning = me.getValue(entry)
            endtablesize+=lt.size(sightning)
            for element in lt.iterator(sightning):
                shape = element['shape']
                if shape == '':
                    shape = 'Unknown'
                endtable.add_row([str(element['datetime']), str(element['city']), str(element['state']), str(element['country']), shape ,str(element['duration (seconds)'])])
    return maintable, endtable, endtablesize

#Req 4
def rangecmp(date, start, end):
    return (datetime.strptime(date,'%Y-%m-%d') > start) and (datetime.strptime(date,'%Y-%m-%d') < end)
def rangekeys(keys,catalog,start, end, cmp):
    numerosightnings = 0
    lst = lt.newList('ARRAY_LIST')
    for item in lt.iterator(keys):
        if cmp(item, start,end):
            size = Return_List_Size(catalog['dateIndex'], item)
            numerosightnings += size
            lt.addLast(lst, item)
    return lst
def Construct_Oldest_Table(catalog):
    oldestdate = om.minKey(catalog['dateIndex'])
    entry = om.get(catalog['dateIndex'], oldestdate)
    oldest = me.getValue(entry)
    oldestsize= lt.size(oldest)
    oldtable=PrettyTable()
    oldtable.field_names = ['date', 'count']
    oldtable.align='l'
    oldtable._max_width= {'date': 15,'count':15}
    oldtable.add_row([str(oldestdate),oldestsize])
    return oldtable
def Construct_Dates_Table(catalog, rangekeys):
    numberofsightnings = 0
    maintable=PrettyTable()
    maintable.field_names = ['datetime','city','state','country','shape', 'duration (seconds)']
    maintable.align='l'
    maintable._max_width= {'datetime': 20,'city':20,'state':20,'country':20,'shape':20, 'duration (seconds)':20}
    for item in lt.iterator(rangekeys):
        entry = om.get(catalog['dateIndex'], item)
        sightning = me.getValue(entry)
        for element in lt.iterator(sightning):
            numberofsightnings+=1
            shape = element['shape']
            if shape == '':
                shape = 'Unknown'
            maintable.add_row([str(element['datetime']), str(element['city']), str(element['state']), str(element['country']), shape ,str(element['duration (seconds)'])])
    return maintable, numberofsightnings
#Req 5

def latitudecmp(longitude, minimum, maximum):
    modlongitude = round(float(longitude), 2)
    return (abs(modlongitude)>abs(minimum)) and (abs(modlongitude)<abs(maximum))
def longitudecmp(long1,long2):
    return long1 < long2
def rangelongitude(keys, catalog,minlong,maxlong,minlat,maxlat,cmp):
    list=lt.newList('ARRAY_LIST', cmpfunction=None)
    for item in lt.iterator(keys):
        dictionary = OrderedDict()
        if item != '':
            if cmp(float(item), minlat,maxlat,):
                longkeys =Return_Values_and_Keys(catalog['latitudeIndex'],item, False)
                dictionary['latitude']=item

                for longitude in lt.iterator(longkeys):
                    if longitude != '':
                        if cmp(float(longitude), minlong,maxlong):
                            dictionary['longitude']=longitude
                            lt.addLast(list, dictionary)
    return list
def Construct_Longitude_Table(catalog, pairs):
    maintable=PrettyTable()
    maintable.field_names = ['datetime','city','state','country','shape', 'duration (seconds)', 'latitude', 'longitude']
    maintable.align='l'
    maintable._max_width= {'datetime': 20,'city':20,'state':20,'country':20,'shape':20, 'duration (seconds)':20,'latitude':20, 'longitude':20}
    numberofsightnings=0
    for item in lt.iterator(pairs):
        entrylat = om.get(catalog['latitudeIndex'], item['latitude'])
        longmap = me.getValue(entrylat)
        entrylong = om.get(longmap, item['longitude'])
        sightnings = me.getValue(entrylong)
        for avistamiento in lt.iterator(sightnings):
            numberofsightnings+=1
            shape = avistamiento['shape']
            if shape == '':
                shape = 'Unknown'
            maintable.add_row([str(avistamiento['datetime']), str(avistamiento['city']), str(avistamiento['state']), str(avistamiento['country']), shape ,str(avistamiento['duration (seconds)']), round(float(avistamiento['latitude']),2),round(float(avistamiento['longitude']),2)])
    return maintable, numberofsightnings
# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista
def comparestrings(one, two):
    if one['country']< two['country']:
        return one
    elif one['country']> two['country']:
        return two
    elif one['country'] ==two['country']:
        if one['city']<two['city']:
            return one
        else:
            return two
def compareDurations(duration1, duration2):
    duration2 = float(duration2)
    duration1 = float(duration1)
    if duration1 > duration2:
        return 1
    elif duration1 == duration2:
        return 0
    else:
        return -1
    
def compareCities(id1, id2):
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1
def compareLongitude(long1,long2):
    long11=float(long1)
    long22=float(long2)
    if (long11 == long22):
        return 0
    elif long11 > long22:
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
def comparetime(date1,date2):
    date11=datetime.strptime(date1, '%H:%M')
    date22=datetime.strptime(date2, '%H:%M')
    if (date11 == date22):
        return 0
    elif (date11 > date22):
        return 1
    else:
        return-1
def compareDates(date1,date2):

    date11=datetime.strptime(str(date1), '%Y-%m-%d')
    date22=datetime.strptime(str(date2), '%Y-%m-%d')
    if (date11 == date22):
        return 0
    elif (date11 > date22):
        return 1
    else:
        return-1
# Funciones de ordenamiento