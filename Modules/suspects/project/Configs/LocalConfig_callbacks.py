'''Info Header Start
Name : LocalConfig_callbacks
Author : Wieland@AMB-ZEPH15
Saveorigin : Project.toe
Saveversion : 2022.35320
Info Header End'''
from typing import Type

def GetConfigSchema(configValue:Type["ConfigValue"], collectionDict:Type["CollectionDict"], collectionList:Type["CollectionList"]) -> dict:

	return {
    	"ProjectPath" : configValue( default = "Projects/Example", typecheck = str) 
		}
		
		
#def GetConfigData():
#	return a jsonString. Can be used to fetch API data or similiar.
#	return ""