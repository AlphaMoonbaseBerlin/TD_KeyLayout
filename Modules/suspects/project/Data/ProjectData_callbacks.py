'''Info Header Start
Name : ProjectData_callbacks
Author : Wieland@AMB-ZEPH15
Saveorigin : Project.toe
Saveversion : 2022.35320
Info Header End'''
from typing import Type

def GetConfigSchema(configModule:"SchemaObjects", configComp:"JsonConfig") -> dict:
	configModule.ConfigValue()
	layerItem = configModule.CollectionDict({
		"Name" : configModule.ConfigValue( 
			default = "CustomItem", typecheck=str),
		"Parameter" : configModule.NamedList( 
			default_member = configModule.ConfigValue( typecheck=(str, float)))
	})
	layer = configModule.NamedList( default_member = layerItem() )
	return {
		"Layer" : configModule.NamedList( 
			default_member = configModule.ConfigValue() )
		}
		
		
#def GetConfigData():
#	return a jsonString. Can be used to fetch API data or similiar.
#	return ""