import gmplot
import numpy
import networkx as nx
import csv
import math

def convertAlltoLtln():
    '''
list of routes. each route is a list with each entry being a tuple (lt,ln,name)
'''
    pass



lor=[[('Nazimabad', 24.911098, 67.028587), ('Bara Maidan', 24.916626, 67.021762),('Lasbela', 24.861462, 67.009939),('Lawrence Road', 24.879406, 67.032892),('Barness Street', 24.866086, 67.01592),('Bandar Road', 24.860808, 67.017838),('Tower', 24.935474, 67.138742)]]


def makeGraph(listofroutes):
    G=nx.DiGraph()
##    with open(file, 'r') as csvfile:
##        f = csv.reader(csvfile)
    for row in listofroutes:
        for i in range(len(row)-1):   ## i is a tuple (lt,ln,name)
            curr=row[i]
            nxt=row[i+1]
            G.add_node(curr[0], pos=(curr[1], curr[2]))
            G.add_node(nxt[0], pos=(nxt[1], nxt[2]))
            G.add_edge(curr[0], nxt[0], weight= math.sqrt((curr[1] - nxt[1])**2 + ((curr[2] - nxt[2])**2)))
    return G



##def genRoute(source, destination, graph):
##'''    source might not be in points
##    calculate the closest point to source. set point = source
##   destination(d) might not be in points
##    add d to G temporarily and add edges from d to the points with distance < 0.5 km
##                    
## get lt, ln of source and destination
##    if source not in graph.nodes:
##        graph.add_node(source, pos=(lt_s, ln_s))'''
##        
##    route = nx.shortest_path(graph, source, destination, 'weight')
##    lt=[]
##    ln=[]
##    for i in route:
##        lt.append(i[0])
##        ln.append(i[1])
##    return (lt, ln)
                                                   
def genRoute(source, destination, graph):
    route = nx.shortest_path(graph, source, destination, 'weight')
    lt=[]
    ln=[]
    for i in route:
        lt.append(G.node[i]['pos'][0])
        ln.append(G.node[i]['pos'][1])
    return (lt,ln,route)
    


def displayMap(lt=[24.891419,24.93688,24.9941,25.000994,24.926917],ln =[67.037888,67.090073,67.158737,67.343445 ,67.390823]):
    cn1=numpy.mean(lt)
    cn2=numpy.mean(ln)
    gmap = gmplot.GoogleMapPlotter(cn1, cn2, 16)
    gmap.plot(lt, ln, 'red', edge_width=5)
    gmap.draw("mymap.html")


##lor=[[('Nazimabad', 24.911098, 67.028587), ('Bara Maidan', 24.916626, 67.021762),('Lasbela', 24.861462, 67.009939),('Lawrence Road', 24.879406, 67.032892),('Barness Street', 24.866086, 67.01592),('Bandar Road', 24.860808, 67.017838),('Tower', 24.935474, 67.138742)]]
##G=makeGraph(lor)
##(lt, ln, r)=genRoute('Barness Street', 'Bandar Road', G)
##displayMap(lt, ln)
