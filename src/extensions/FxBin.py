import json

class FxBin:
	def __init__(self, owner):
		self.owner = owner
		self.Presets = owner.op('Presets')
	def SavePreset(self, chain):
		c = self.Presets.copy(self.Presets.op('selector'))
		c.par.Name = 'New Preset'
		c.op('preset').text = json.dumps(chain)
		c.op('field_Name').openViewer()
		c.par.display = True