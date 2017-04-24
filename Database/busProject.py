import pypyodbc

connection = pypyodbc.connect('Driver={SQL Server};'
                                'Server=localhost;'
                                'Database=PublicTransportPortal;'
                                'uid=sa;pwd=password')
cursor = connection.cursor() 
SQLCommand = ("SELECT idBus FROM Bus")
cursor.execute(SQLCommand)
results = cursor.fetchone()
while results:
    print ("Your customer " +  str(results[0]))
    results = cursor.fetchone()



cursor = connection.cursor()
SQLCommand = ("INSERT INTO Bus (idBus,source,destination,bus_type) values (?,?,?,?)")
Values = ['17-H ','Saddar', 'Dhobi Ghat','Bus']
cursor.execute(SQLCommand,Values)
connection.commit()

connection.close()
