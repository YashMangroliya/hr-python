from hr import HRDLHandler,DataLayerException,DBConnection
import sys
try:
    code=int(sys.argv[1])
    HRDLHandler.delete_designation(code)
    print("Designation deleted")
except DataLayerException as dataLayerException:
    print(dataLayerException.message)
    print(dataLayerException.exceptions)