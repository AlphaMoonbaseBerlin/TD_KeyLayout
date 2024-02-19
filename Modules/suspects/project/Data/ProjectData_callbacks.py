'''Info Header Start
Name : ProjectData_callbacks
Author : Wieland@AMB-ZEPH15
Saveorigin : Project.toe
Saveversion : 2022.35320
Info Header End'''
from typing import Type

def GetConfigSchema(configModule:"Type[SchemaObjects]", configComp:"JsonConfig") -> dict:
	
	LayerItem = configModule.CollectionDict({
		#"Name" : configModule.ConfigValue( default = "", typecheck = str, comment = """The name of the Item. Needs to be Unique!"""),
		"Prefab" : configModule.ConfigValue( default = "", typecheck = str, comment = """The prefab that should be loaded."""),
		"Arguments" : configModule.NamedList( 
			default_member = configModule.ConfigValue(
				default = "",
				typecheck = (str, float, int),
				comment = "Key Valuepair describing a Parameter of the prefab."
			))
	})

	LayerObject = configModule.CollectionDict({
		#"Name" : configModule.ConfigValue( default = "", typecheck = str, comment = """The name of the Layer. Needs to be Unique!"""),
		"Default" : configModule.ConfigValue( default = ""),
		"Transition" : configModule.ConfigValue( default = 0.7),
		"Hold" : configModule.ConfigValue( default = 5),
		"FadeOverBlack" : configModule.ConfigValue( default = False),
		"Presets" : configModule.NamedList(
			default_member = configModule.CollectionList(
				default_member = configModule.ConfigValue(default = "", typecheck = str),
				comment = "A list of Items which an be preselected."
			)
		),
		"Items": configModule.NamedList( default_member = LayerItem() )
	})
	return {
		"ProjectName" : configModule.ConfigValue( default = "My Project", comment = "A descriptive name. Not really needed."),

		"Layer" : configModule.NamedList( default_member = LayerObject())
		}
		
		
#def GetConfigData():
#	return a jsonString. Can be used to fetch API data or similiar.
#	return ""