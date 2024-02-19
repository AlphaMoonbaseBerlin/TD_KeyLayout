'''Info Header Start
Name : extLayerPlayerController
Author : Wieland@AMB-ZEPH15
Saveorigin : Project.toe
Saveversion : 2022.35320
Info Header End'''

tweener = op("tweenerDependency").GetGlobalComponent()
class extLayerPlayerController:
	"""
	extLayerPlayerController description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp

	@property
	def Layer(self):
		return self.ownerComp.par.Target.eval()

	@property
	def Active(self):
		return { item for item in self.Layer.findChildren( depth = 1) if item.par.Level.eval() not in [0,2] }

	@property
	def Selected(self):
		return [ self.Layer.op( name ) for name in self.ownerComp.op("selectedItems").col(0) ]
	
	@property
	def Available(self):
		return [ self.Layer.op( name ) for name in self.ownerComp.op("opfind1").col("name")[1:] ]

	def PlayNext(self, fadeoutActive = False):
		if fadeoutActive: self.FadeoutActive()
		currentIndex = int( op("playlistState")["currentIndex"].eval() )
		nextIndex = ( currentIndex + 1 ) % self.ownerComp.op("selectedItems").numRows
		self._fadeIn(
			self.Layer.op( self.ownerComp.op("selectedItems")[nextIndex, 0] )
		)
		self.ownerComp.op("playlistState").par.value0.val = nextIndex

	def FadeoutActive(self, ignoreComp = None):
		for item in self.Active - {ignoreComp}:
			self._fadeOut( item )

	def Select(self, name:str):
		targetItem = self.Layer.op( name )
		self.FadeoutActive( ignoreComp = targetItem)
		if targetItem: self._fadeIn( targetItem )

	def _fadeOut(self, target):
		tweener.RelativeTween(
			target.par.Level,
			2,
			1/self.ownerComp.par.Transition.eval()
		)

	def _fadeIn(self, target):
		if target not in self.Active: target.par.Level.val = 0
		tweener.RelativeTween(
			target.par.Level,
			1,
			1/self.ownerComp.par.Transition.eval()
		)

	def _addItem(self, itemName):
		self.ownerComp.op("selectedItems").appendRow( itemName )
	
	def _removeItem(self, itemName):
		self.ownerComp.op("selectedItems").deleteRow( itemName )

	def ToggleItem(self, itemName):
		if self.ownerComp.op("selectedItems")[ itemName, 0]:
			self._removeItem( itemName )
		else:
			self._addItem( itemName )
	
	@property
	def Presets(self):
		return [key for key in iop.Store.Data.op("ProjectData").Data.Layer[self.ownerComp.par.Name.eval()].Presets.keys()]
	
	def RecallPreset(self, presetName):
		self.ownerComp.op("selectedItems").clear()
		self.ownerComp.op("selectedItems").appendRows(
			iop.Store.Data.op("ProjectData").Data.Layer[self.ownerComp.par.Name.eval()].Presets[presetName]
		)