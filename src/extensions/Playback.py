class Playback:
	def __init__(self, owner):
		self.owner = owner
		self.owner.store('scenes', self.owner.fetch('scenes', []))
	def Scenes(self):
		return self.owner.fetch('scenes', [])
	def SwitchScene(self, name):
		scenes = self.Scenes()[:]
		for i,s in enumerate(scenes):
			if s.name == self.owner.par.Active.eval():
				s.name = name
				break
		self.owner.store('scenes', scenes)
	def OpenScene(self, name):
		scenes = self.Scenes()[:]
		op = self.owner.copy(self.owner.op('__EMPTY__'), name=name)
		op.par.Scene = name
		scenes.append(op)
		self.owner.store('scenes', scenes)
	def KillScene(self, name):
		op = None
		scenes = self.Scenes()[:]
		if len(scenes) <= 1:
			return
		for i,s in enumerate(scenes):
			if s.name == name:
				if i == 0:
					self.owner.par.Active = scenes[1].name
				else:
					self.owner.par.Active = scenes[i-1].name
				op = scenes.pop(i)
				break
		self.owner.store('scenes', scenes)
		op.destroy()