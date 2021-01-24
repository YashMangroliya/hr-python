from xml.etree import ElementTree
from os import path
from mysql.connector import connect,Error

class DataLayerException(Exception):
    def __init__(self,message="",exceptions=None):
        self.message=message
        self.exceptions=exceptions

class DBConfiguration:
    def __init__(self,host,port,database,user,password):
        self.exceptions=dict()
        self.host=host
        self.port=port
        self.database=database
        self.user=user
        self.password=password
        self.has_exceptions=False
        self._validate_values();
    def _validate_values(self):
        if isinstance(self.host,str)==False:
            self.exceptions["host"]=('T',f"host is of type {type(self.host)}, should be of type {type('A')}")
        if isinstance(self.port,int)==False:
            self.exceptions["port"]=('T',f"port is of type {type(self.port)}, should be of type {type(10)}")
        if isinstance(self.database,str)==False:
            self.exceptions["database"]=('T',f"database is of type {type(self.database)}, should be of type {type('A')}")
        if isinstance(self.user,str)==False:
            self.exceptions["user"]=('T',f"user is of type {type(self.user)}, should be of type {type('A')}")
        if isinstance(self.password,str)==False:
            self.exceptions["password"]=('T',f"password is of type {type(self.password)}, should be of type {type('A')}")

        if ("host" in self.exceptions)==False and len(self.host)==0:
            self.exceptions["host"]=('V',"host ip/name missing")
        if ("port" in self.exceptions)==False and (self.port<=0 or self.port>=65535):
            self.exceptions["port"]=('V',f"value of port is {self.port}, should be greater than 0 and less than 65535")
        if ("database" in self.exceptions)==False and len(self.database)==0:
            self.exceptions["database"]=('V',"database missing")
        if ("user" in self.exceptions)==False and len(self.user)==0:
            self.exceptions["user"]=('V',"username missing")
        if ("password" in self.exceptions)==False and len(self.password)==0:
            self.exceptions["password"]=('V',"password missing")
        if len(self.exceptions)>0:
            self.has_exceptions=True

class DBUtility:
    def getDBConfiguration(self):
        if path.isfile('dbconfig.xml')==False : raise DataLayerException("dbconfig.xml with database connection details is missing, refer documentation")
        f=open('dbconfig.xml','rt')
        try:
            xmlTree=ElementTree.parse(f)
        except ElementTree.ParseError as parseError:
            raise DataLayerException("dbconfig.xml with database connection is malformed")
        finally:
            f.close()
        rootNode=xmlTree.getroot()
        host=None
        port=None
        database=None
        user=None
        password=None
        for node in rootNode:
            if node.tag=="host": host=node.text
            if node.tag=="port": port=node.text
            if node.tag=="name": database=node.text
            if node.tag=="user": user=node.text
            if node.tag=="password": password=node.text
        dbConfiguration=DBConfiguration(host,int(port),database,user,password)
        if dbConfiguration.has_exceptions: raise DataLayerException(exceptions=dbConfiguration.exceptions)
        return dbConfiguration


class DBConnection:
    def getConnection():
        dbUtility=DBUtility()
        dbConfiguration=dbUtility.getDBConfiguration()
        if dbConfiguration.has_exceptions: raise DataLayerException(exceptions=dbConnection.exceptions)
        try:
            connection=connect(host=dbConfiguration.host,port=dbConfiguration.port,database=dbConfiguration.database,user=dbConfiguration.user,password=dbConfiguration.password)
            return connection
        except Error as error:
            raise DataLayerException(error.msg) 	

class Designation:
    def __init__(self,code,title):
        self.exceptions=dict()
        self.has_exceptions=False
        self.code=code
        self.title=title
        self._validate_values()
    def _validate_values(self):
        if(isinstance(self.code,int)==False):
            self.exceptions["code"]=('T',f"Code is of type {type(self.code)}, it should be of type {type(10)}")
        if(isinstance(self.title,str)==False):
            self.exceptions["title"]=('T',f"Title is of type {type(self.title)}, it should be of type {type('A')}")
        if(("code" in self.exceptions)==False and self.code<0):
            self.exceptions["code"]=('V',f"Value of code is {self.code}, it should be >=0")
        if(("title" in self.exceptions)==False):
            lengthOfTitle=len(self.title)
            if(lengthOfTitle==0 or lengthOfTitle>35):
                self.exceptions["title"]=('V',f"Length of title should be greater than 0 and less than 36")
        if(len(self.exceptions)>0):
            self.has_exceptions=True

class HRDLHandler:
    def add_designation(designation):
        if designation==None: raise DataLayerException("Designation required")
        if isinstance(designation,Designation)==False: raise DataLayerException(f"Designation type found {type(designation)},required {type(Designation)}")
        if designation.has_exceptions: raise DataLayerException(exceptions=designation.exceptions)
        if designation.code!=0: raise DataLaterException("Designation code should be 0 as it is auto generated")
        try:
            dbConnection=DBConnection.getConnection()
            cursor=dbConnection.cursor()
            cursor.execute("select code from designation where title=%s",(designation.title,))
            rows=cursor.fetchall()
            if len(rows)>0: raise DataLayerException(f"{designation.title} exists")
            cursor.execute("insert into designation (title) values (%s)",(designation.title,))
            designation.code=cursor.lastrowid
            dbConnection.commit()
        except Error as error:
            raise DataLayerException(error.msg)
        finally:
            try:
                if cursor.is_open(): cursor.close()
                if dbConnection.is_connected(): dbConnection.close()
            except:
                pass


    def update_designation(designation):
        if designation==None: raise DataLayerException("D-esignation required")
        if isinstance(designation,Designation)==False: raise DataLayerException(f"Designation type required {type(Designation)}, found {type(designation)}")
        if designation.has_exceptions: raise DataLayerException(exceptions=designation.exceptions)
        if designation.code==0: raise DataLayerException("Designation code can not be 0")
        try:
            dbConnection=DBConnection.getConnection()
            cursor=dbConnection.cursor()
            cursor.execute("select title from designation where code=%s",(designation.code,))
            rows=cursor.fetchall()
            if len(rows)==0: raise DataLayerException(f"Designation code {designation.code} does not exists")
            cursor.execute("select code from designation where title=%s and code<>%s",(designation.title,designation.code))  # <> represents 'not equal to'
            rows=cursor.fetchall()
            if len(rows)>0: raise DataLayerException(f"Designation title {designation.title} already exists.")
            cursor.execute("update designation set title=%s where code=%s",(designation.title,designation.code))            
            dbConnection.commit()
        except Error as error:
            raise DataLayerException(error.msg)
        finally:
            try:
                if cursor.is_open(): cursor.close()
                if dbConnection.is_connected(): dbConnection.close()
            except:
                pass
                
    def delete_designation(code):
        if code==None: raise DataLayerException(f"Invalid code: {code}")
        if code<=0: raise DataLayerException(f"Invalid code: {code}")
        try:
            dbConnection=DBConnection.getConnection()
            cursor=dbConnection.cursor()
            cursor.execute("select code from designation where code=%s",(code,))
            rows=cursor.fetchall()
            if len(rows)==0: raise DataLayerException(f"Invalid code: {code}")
            cursor.execute("delete from designation where code=%s",(code,))
            dbConnection.commit()
        except Error as error:
            raise DataLayerException(error.msg)
        finally:
            try:
                if cursor.is_open(): cursor.close()
                if dbConnection.is_connected(): dbConnection.close()
            except:
                pass


    def getDesignations():
        designations=list()
        try:
            dbConnection=DBConnection.getConnection()
            cursor=dbConnection.cursor()
            cursor.execute("select * from designation order by title")
            rows=cursor.fetchall()
            for row in rows:
                designations.append(Designation(row[0],row[1]))
            dbConnection.commit()
            return designations
        except Error as error:
            raise DataLayerException(error.msg)
        finally:
            try:
                if cursor.is_open(): cursor.close()
                if dbConnection.is_connected(): dbConnection.close()
            except:
                pass


    def getByCode(code):
        pass
    def getByTitle(title):
        pass 