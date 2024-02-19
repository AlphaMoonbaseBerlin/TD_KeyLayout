'''Info Header Start
Name : extDataManager
Author : Wieland@AMB-ZEPH15
Saveorigin : Project.toe
Saveversion : 2022.35320
Info Header End'''

class InvalidPath():
	pass


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
		self._clear( self.ownerComp.op("Prefabs"), compType= geometryCOMP )

	def _clear(self, comp, compType = baseCOMP):
		for item in comp.findChildren( depth = 1, type = compType ):
			if item.valid: item.destroy()

	def _loadItems(self, projectPath):
		projectPathObject = Path( projectPath )
		for subElement in projectPathObject.iterdir():
			if not subElement.is_dir(): continue
			elementOp = self.ownerComp.op("Items").copy(
				self.ownerComp.op("folderPrefab"),
				name = subElement.stem
			)
			elementOp.par.Rootfolder.val = subElement

	def _loadPrefabs(self, projectPath):
		projectPathObject = Path( projectPath, "prefabs" )
		for subElement in projectPathObject.iterdir():
			if subElement.is_dir() or subElement.suffix != ".tox": continue
			elementOp = self.ownerComp.op("Prefabs").loadTox(
				subElement
			)
			elementOp.par.externaltox.val = subElement
			elementOp.name = subElement.stem

	def LoadProject(self):
		projectPath = self.ownerComp.par.Project.eval()
		self._clearItems()
		self._loadItems( projectPath )
		self._clearPrefabs()
		self._loadPrefabs( projectPath )

	def _clearLayout(self):
		self._clear( iop.Store.Layout, compType = geometryCOMP )

	def LoadLayout(self):
		self._clearLayout()
		for layerIndex, (layerName, layerData) in  enumerate( self.ownerComp.op("ProjectData").Data.Layer.items() ):
			layerObject = iop.Store.Layout.create( geometryCOMP, layerName, initialize=False )
			layerObject.render = True
			layerObject.par.drawpriority.val = layerIndex
			layerObject.par.tz.val = -layerIndex
			layerObject.nodeY = layerIndex * 260
			for itemIndex, (itemName, itemData) in enumerate( layerData.Items.items() ):
				itemObject = layerObject.create( geometryCOMP, itemName, initialize=False )
				itemObject.par.drawpriority.val = itemIndex
				itemObject.par.tz.val = -itemIndex
				itemObject.render = True
				itemObject.par.clone.val = self.Prefab( itemData.Prefab )
				itemObject.par.enablecloningpulse.pulse()
				for customPar in itemObject.customPars: customPar.val = customPar.default
				itemObject.nodeY = itemIndex * 260
				for argumentName, argumentValue in itemData.Arguments.items():
					parameter:Par = getattr( itemObject.par, argumentName )
					parameter.bindExpr = f"iop.Store.Data.op('ProjectData').Data.Layer.{layerName}.Items.{itemName}.Arguments.{argumentName}.Dependency"
			layerObject.par.sz.val = 1/(len(layerData.Items) + 1)
			if layerData.Default.Value:
				layerObject.op(layerData.Default.Value).par.Level = 1
		pass

	def Asset(self, name):
		try:
			splitPath = name.split("/")
			category = splitPath[0]
			relPath = "/".join( splitPath[1:] )
			return Path( str(self.ownerComp.op("Items").op(category).op("data")[ relPath, "path"]) )
		except AttributeError:
			return InvalidPath()
		
	def Prefab(self, name):
		return self.ownerComp.op("Prefabs").op(name)