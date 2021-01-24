from hr import DBUtility,DataLayerException
try:
    dbConfiguration=DBUtility().getDBConfiguration()
except DataLayerException as dataLayerException:
    print(dataLayerException.message)
    print(dataLayerException.exceptions)