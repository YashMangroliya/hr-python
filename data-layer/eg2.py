from hr import DBConfiguration
dbConfiguration=DBConfiguration(host="localhost",port=5500,database="hrdb",user="hr",password="hr")
if dbConfiguration.has_exceptions: print(dbConfiguration.exceptions)