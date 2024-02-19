'''Info Header Start
Name : extDataManager
Author : Wieland@AMB-ZEPH15
Saveorigin : Project.toe
Saveversion : 2022.35320
Info Header End'''

from pathlib import Path
class extDataManager:
	"""
	extDataManager description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp

	def _clearItems(self):
		self._clear( self.ownerComp.op("Items"))

	def _clearPrefabs(self):
		self._clear( self.ownerComp.op("Prefabs") )

	def _clear(self, comp):
		for item in comp.findChildren( depth = 1 ):
			if item.valid: item.destroy()

	def _loadItems(self, projectPath):
		projectPathObject = Path( projectPath )
		for subElement in projectPathObject.iterdir():
			if not subElement.is_dir(): continue
			elementOp = self.ownerComp.op("Items").copy(
				self.ownerComp.op("folderPrefab"),
				name = subElement.stem
			)
			elementOp.par.rootfolder.val = subElement

	def LoadProject(self, projectPath:str):
		self._clearItems()
		self._loadItems( projectPath )

	def Asset(self, category, name):
		return Path( str(self.ownerComp.op("Items").op(category)[ name, "path"]) )
	
	def Prefab(self, name):
		return self.ownerComp.op("Prefabs").op(name)