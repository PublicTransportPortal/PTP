import urllib
import urllib.request
import json
import io
import csv

def decodeAddressToCoordinates( address ):
        urlParams = {
                'address': address,
                'sensor': 'false',
                'key': 'AIzaSyC0YPb9g1-4gIC-S4EySodz5OHcUw1zzVo'
        }  
        url = 'https://maps.google.com/maps/api/geocode/json?' + urllib.parse.urlencode( urlParams )
        response = urllib.request.urlopen( url )
        responseBody = response.read().decode('utf-8')
        body = io.StringIO( responseBody )
        result = json.load( body )
        if 'status' not in result or result['status'] != 'OK':
                return None
        else:
                return {
                        'lat': result['results'][0]['geometry']['location']['lat'],
                        'lng': result['results'][0]['geometry']['location']['lng']
                }
        
def makeLatLongCsv():
    latLongList = []
    with open('routes.csv', 'r') as csvfile:
        #routesReader = csv.reader(csvfile)
        listOfRoutes = list(list(rec) for rec in csv.reader(csvfile, delimiter=','))
    csvfile.close()
    for i in range(0, 80):
        routesRow = listOfRoutes[i]
        latLongRow = routesRow[:2]
        for j in range(2,len(routesRow)):
            latLongDict = decodeAddressToCoordinates(routesRow[j] + ", Karachi")
            if latLongDict is None:
                print (routesRow[j],latLongDict, i, j)
                latLongRow.append("None")
            else:
                latLongRow.append((latLongDict["lng"], latLongDict["lat"]))
        latLongList.append(latLongRow)
    with open("latlong.csv", "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(latLongList)
    csvfile.close()
                
        

