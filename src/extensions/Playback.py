class Playback:
	def __init__(self, owner):
		self.owner = owner
		self.owner.store('scenes', self.owner.fetch('scenes', []))
	def indexBySid(self, sid):
		idx = -1
		scenes = self.Scenes()
		for i,s in enumerate(scenes):
			if s.par.Scene.eval() == sid:
				idx = i
		return idx
	def ActiveBrowser(self):
		scenes = self.Scenes()
		for i,s in enumerate(scenes):
			if s.par.Scene.eval() == self.owner.par.Active.eval():
				return s
		return None
	def Scenes(self):
		return self.owner.fetch('scenes', [])
	def SwitchScene(self, sid):
		print(sid)
		scenes = self.Scenes()[:]
		existsAt = self.indexBySid(sid)
		if existsAt >= 0:
			self.owner.par.Active = sid
			self.owner.op('tabs').par.Value0 = existsAt
			return
		for i,s in enumerate(scenes):
			if s.par.Scene.eval() == self.owner.par.Active.eval():
				s.par.Scene = sid
				break
		self.owner.store('scenes', scenes)
		self.owner.par.Active = sid
	def OpenScene(self, sid):
		scenes = self.Scenes()[:]
		existsAt = self.indexBySid(sid)
		if existsAt >= 0:
			self.owner.par.Active = sid
			self.owner.op('tabs').par.Value0 = existsAt
			return
		op = self.owner.copy(self.owner.op('__EMPTY__'), name="browser0")
		op.par.Scene = sid
		scenes.append(op)
		self.owner.store('scenes', scenes)
	def KillScene(self, sid):
		op = None
		scenes = self.Scenes()[:]
		destTab = 0
		if len(scenes) <= 1:
			return
		for i,s in enumerate(scenes):
			if s.par.Scene.eval() == sid:
				if i == 0:
					self.owner.par.Active = scenes[1].par.Scene.eval()
				else:
					self.owner.par.Active = scenes[i-1].par.Scene.eval()
					destTab = i - 1
				op = scenes.pop(i)
				break
		self.owner.store('scenes', scenes)
		self.owner.op('tabs').par.Value0 = destTab
		op.destroy()