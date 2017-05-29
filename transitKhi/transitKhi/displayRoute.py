import gmplot
import numpy
import networkx as nx
import csv
import math
import requests
import matplotlib.pyplot as plt
import urllib
import urllib.request
import json
import io
from fuzzywuzzy import fuzz

class BestRoute(object):

    def __init__(self, source, destination):
        self.source = source
        self.destination = destination
        with open('routes.csv', 'r') as csvfile:
            self.listOfRoutes = list(list(rec) for rec in csv.reader(csvfile, delimiter=','))
        csvfile.close()
        with open('latLong.csv', 'r') as csvfile:
            self.listOfLatLong = list(list(rec) for rec in csv.reader(csvfile, delimiter=','))
        csvfile.close()
        self.mainList = []
        self.busList = []
        self.locationList = []
        self.graph = nx.Graph()

    def __str__(self):
        return 'Parser object'

    def getRoutes(self):
        for i in range(len(self.listOfLatLong)):
            routesRow = self.listOfRoutes[i]
            latlongRow = self.listOfLatLong[i]
            routesList = []
            self.busList.append(routesRow[0])
            for j in range(2,len(latlongRow)):
                location = routesRow[j].strip().strip(".")
                latlong = latlongRow[j]
                if latlong != "None" and latlong != "":
                    commaFind = latlong.find(",")
                    #print (i, j, location, latlong, len(latlong), commaFind)
                    longitude = float(latlongRow[j][1:commaFind])
                    latitude = float(latlongRow[j][commaFind+1:-1])
                    if latitude > 24.7 and latitude < 25.1 and longitude > 66.8 and longitude < 67.4:   
                        routesList.append((location, latitude, longitude))
            self.mainList.append(routesList)

    def makeLocationList(self):
        for row in self.mainList:
            for location in row:
                if location not in self.locationList:
                    self.locationList.append(location)

    def makeGraph(self):
        uniqueLocationList = []
        for row in self.mainList:
            curr = row[0]
            if curr not in uniqueLocationList:
                self.graph.add_node(curr[0], pos = (curr[1], curr[2]))
                uniqueLocationList.append(curr)
            for i in range(len(row)-1): 
                nxt = row[i+1]
                if nxt not in uniqueLocationList:
                    self.graph.add_node(nxt[0], pos = (nxt[1], nxt[2]))
                    uniqueLocationList.append(nxt)
                self.graph.add_edge(curr[0], nxt[0], weight = math.sqrt((curr[1] - nxt[1])**2 + ((curr[2] - nxt[2])**2)))
                curr = nxt
    
    def decodeAddressToCoordinates(self, address):
        urlParams = {'address': address,
                     'sensor': 'false'}  
        url = 'http://maps.google.com/maps/api/geocode/json?' + urllib.parse.urlencode( urlParams )
        response = urllib.request.urlopen( url )
        responseBody = response.read().decode('utf-8')
        body = io.StringIO( responseBody )
        result = json.load( body )
        if 'status' not in result or result['status'] != 'OK':
            return None
        else:
            return {'lat': result['results'][0]['geometry']['location']['lat'],
                    'lng': result['results'][0]['geometry']['location']['lng']}

    def getMatchingLocations(self, place):
        matchingList = []
        for loc in self.locationList:
            location = loc[0]
            partialRatio = fuzz.partial_ratio(place, location)
            sortRatio = fuzz.token_sort_ratio(place, location)
            setRatio = fuzz.token_set_ratio(place, location)
            if (partialRatio + sortRatio + setRatio) >= 200:
                matchingList.append(location)
        return matchingList

    def findClosestNode(self, lat, long):
        minDist = 1000
        for i in self.locationList:
            locationLat = i[1]
            locationLong = i[2]
            dist = math.sqrt((locationLat - lat)**2 + (locationLong - long)**2)
            if dist < minDist:
                closestNode = i[0]
                minDist = dist
        return (closestNode, minDist)

    def genRoute(self, source, destination):
        self.route = nx.shortest_path(self.graph, source, destination, 'weight')
        lt = []
        ln = []
        for i in self.route:
            lt.append(self.graph.node[i]['pos'][0])
            ln.append(self.graph.node[i]['pos'][1])
        return (lt,ln)

    def genBuses(self):
        contenderList = []
        for i in range(len(self.route)-1):
            current = self.route[i]
            nxt = self.route[i+1]
            contenderBuses = self.findBus(current, nxt)
            if len(contenderList) == 0:
                for bus in contenderBuses:
                    contenderList.append([(bus, [current, nxt])])
            else:
                newContenderList = []
                for contender in contenderList:
                    for bus in contenderBuses:
                        idx = contenderList.index(contender)
                        if bus == contender[-1][0]:
                            newBusList = contender[-1][1] + [nxt]
                            newContender = contender[:-1] + [(bus, newBusList)]
                        else:
                            newContender = contender + [(bus, [current, nxt])]
                        newContenderList = newContenderList + [newContender]
                contenderList = newContenderList
        bestList = self.getBest(contenderList)
        return bestList

    def getBest(self, contenderList):
        bestList = contenderList[0]
        bestLen = len(bestList)
        for contender in contenderList[1:]:
            if len(contender) < bestLen:
                bestList = contender
                bestLen = len(bestList)
        for bus in bestList:
            idx = bestList.index(bus)
            bestList[idx] = (bus[0], [bus[1][0], bus[1][-1]])
        return bestList

    def findBus(self, current, nxt):
        contenderBuses = []
        for busRoute in self.mainList:
            newBusRoute = [seq[0] for seq in busRoute]
            if self.contains([current, nxt], newBusRoute) or self.contains([nxt, current], newBusRoute) :
                contenderBuses.append(self.busList[self.mainList.index(busRoute)])
        return contenderBuses

    def contains(self, small, big):
        for i in range(len(big)-len(small)+1):
            for j in range(len(small)):
                if big[i+j] != small[j]:
                    break
            else:
                return True
        return False

    def displayMap(self, lt, ln):
        cn1 = numpy.mean(lt)
        cn2 = numpy.mean(ln)
        gmap = gmplot.GoogleMapPlotter(cn1, cn2, 16)
        gmap.plot(lt, ln, 'red', edge_width=5)
        gmap.draw("C:\\Users\\fatim\\OneDrive for Business\\Semester6\\SE\\New folder\\TransitHTML\\templates\\mymap.html") #file path to template folder

    def generatePathString(self):
        self.getRoutes()
        self.makeLocationList()
        sourceLatLong = self.decodeAddressToCoordinates(self.source + ", Karachi")
        destinationLatLong = self.decodeAddressToCoordinates(self.destination + ", Karachi")
        sourceMatchingList = self.getMatchingLocations(self.source)
        destinationMatchingList = self.getMatchingLocations(self.destination)
        if sourceLatLong is None:
            if sourceMatchingList == []:
                return "Error: your source location is invalid. Please re-enter your source location."
            else:
                return "For source location, did you mean: " + " or ".join(sourceMatchingList)
        if destinationLatLong is None:
            if destinationMatchingList == []:
                return "Error: your destination location is invalid. Please re-enter your destination location."
            else:
                return "For destination location, did you mean: " + " or ".join(destinationMatchingList)
        sourceLat = sourceLatLong["lat"]
        sourceLong = sourceLatLong["lng"]
        destinationLat = destinationLatLong["lat"]
        destinationLong = destinationLatLong["lng"]
        if sourceLat == destinationLat and sourceLong == destinationLong:
            return "You have entered the same location for source and destination."
        (start, startDist) = self.findClosestNode(sourceLat, sourceLong)
        (end, endDist) = self.findClosestNode(destinationLat, destinationLong)
        if startDist >= 0.05:
            if sourceMatchingList == []:
                return "Error: your source location is outside Karachi. Please re-enter your source location."
            else:
                return "For source location, did you mean: " + " or ".join(sourceMatchingList)
        if endDist >= 0.05:
            if destinationMatchingList == []:
                return "Error: your destination location is outside Karachi. Please re-enter your destination location."
            else:
                return "For destination location, did you mean: " + " or ".join(destinationMatchingList)
        self.makeGraph()
        (lat, long) = self.genRoute(start, end)
        self.displayMap(lat, long)
        buses = self.genBuses()
        startPoint = buses[0][1][0]
        endPoint = buses[-1][1][-1]
        startPointLatLong = self.decodeAddressToCoordinates(startPoint + ", Karachi")
        endPointLatLong = self.decodeAddressToCoordinates(endPoint + ", Karachi")
        if startPointLatLong == sourceLatLong:
            startWalk = ""
        else:
            startWalk = "Walk from " + self.source + " to " + startPoint + ". "
        if endPointLatLong == destinationLatLong:
            endWalk = ""
        else:
            endWalk = "Walk from " + endPoint + " to " + self.destination + "."
        busPath = ""
        for bus in buses:
            busName = bus[0]
            busFind = busName.find("\xa0")
            if busFind != -1:
                busName = busName[:busFind]
            busPath += "Take " + busName + " from " + bus[1][0] + " to " + bus[1][1] + ". "
        return (startWalk + busPath + endWalk)

def main(source, destination):
    br = BestRoute(source, destination)
    return br.generatePathString()

def checkTestCases():
    case1 = main("Malir", "Singapore")
    case2 = main("abcdefghi", "a")
    case3 = main("Korangi", "Beemari")
    case4 = main("  Karimabad", "karimabad")
    case5 = main("Aga Khan Hospital", "Habib Univeristy")
    print ('Test Case 1: main("Malir", "Singapore")')
    print ('Output: ' + case1)
    if case1 == 'Error: your destination location is outside Karachi. Please re-enter your destination location.':
        print ('Test Passed')
    else:
        print ('Test Failed')
    print ('Test Case 2: main("abcdefghi", "a")')
    print ('Output: ' + case2)
    if case2 == 'Error: your source location is invalid. Please re-enter your source location.':
        print ('Test Passed')
    else:
        print ('Test Failed')
    print ('Test Case 3: main("Korangi", "Beemari")')
    print ('Output: ' + case3)
    if 'For destination location, did you mean:' in case3:
        print ('Test Passed')
    else:
        print ('Test Failed')
    print ('Test Case 4: main("  Karimabad", "karimabad")')
    print ('Output: ' + case4)
    if case4 == 'You have entered the same location for source and destination.':
        print ('Test Passed')
    else:
        print ('Test Failed')
    print ('Test Case 5: main("Aga Khan Hospital", "Habib Univeristy")')
    print ('Output:' , case5)
    if "Take" in case5:
        print ('Test Passed')
    else:
        print ('Test Failed')


