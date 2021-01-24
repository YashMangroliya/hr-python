from hr import HRDLHandler,DataLayerException,DBConnection
import sys
try:
    designations=HRDLHandler.getDesignations()
    for designation in designations:
        print(f"Code: {designation.code}, Title: {designation.title}")
except DataLayerException as dataLayerException:
    print(dataLayerException.message)
    print(dataLayerException.exceptions)