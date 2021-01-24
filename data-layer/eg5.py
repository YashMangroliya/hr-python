from hr import HRDLHandler,DataLayerException,Designation
try:
    designation=Designation(0,"Sports Teacher")
    HRDLHandler.add(designation)
except DataLayerException as dataLayerException:
    print(dataLayerException.message)
    print(dataLayerException.exceptions)
    