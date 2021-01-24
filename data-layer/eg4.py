from hr import DBConnection,DataLayerException
try:
    dbConnection=DBConnection().getConnection()
except DataLayerException as dataLayerException:
    print(dataLayerException.message)
    print(dataLayerException.exceptions)