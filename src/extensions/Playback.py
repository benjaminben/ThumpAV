class Playback:
	def __init__(self, owner):
		self.owner = owner
		self.owner.store('scenes', self.owner.fetch('scenes', []))
	def indexByName(self, name):
		idx = -1
		scenes = self.Scenes()
		for i,s in enumerate(scenes):
			if s.name == name:
				idx = i
		return idx
	def Scenes(self):
		return self.owner.fetch('scenes', [])
	def SwitchScene(self, name):
		scenes = self.Scenes()[:]
		existsAt = self.indexByName(name)
		if existsAt >= 0:
			self.owner.par.Active = name
			self.owner.op('tabs').par.Value0 = existsAt
			return
		for i,s in enumerate(scenes):
			if s.name == self.owner.par.Active.eval():
				s.name = name
				break
		self.owner.store('scenes', scenes)
		self.owner.par.Active = name
	def OpenScene(self, name):
		scenes = self.Scenes()[:]
		existsAt = self.indexByName(name)
		if existsAt >= 0:
			self.owner.par.Active = name
			self.owner.op('tabs').par.Value0 = existsAt
			return
		op = self.owner.copy(self.owner.op('__EMPTY__'), name=name)
		scenes.append(op)
		self.owner.store('scenes', scenes)
	def KillScene(self, name):
		op = None
		scenes = self.Scenes()[:]
		destTab = 0
		if len(scenes) <= 1:
			return
		for i,s in enumerate(scenes):
			if s.name == name:
				if i == 0:
					self.owner.par.Active = scenes[1].name
				else:
					self.owner.par.Active = scenes[i-1].name
					destTab = i - 1
				op = scenes.pop(i)
				break
		self.owner.store('scenes', scenes)
		self.owner.op('tabs').par.Value0 = destTab
		op.destroy()