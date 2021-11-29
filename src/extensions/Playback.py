class Playback:
	def __init__(self, owner):
		self.owner = owner
	def OpenScene(self, name):
		b = self.owner.op(f'browser{self.owner.par.Active.eval()}')
		b.par.Scene = name
		items = self.owner.par.Scenes.eval()
		items[self.owner.par.Active.eval()] = name
		self.owner.par.Scenes = items