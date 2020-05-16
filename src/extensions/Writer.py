Launcher = op(ipar.LiveLauncher)

class Writer:
	def __init__(self, owner):
		self.owner = owner
		return
	def WriteSource(self, cue):
		for i,t in enumerate(cue['tracks']):
			if i == 0:
				continue
			t["source"] = Launcher.op('bus{}/file'.format(i)).par.file.eval()
		return cue
	def WriteOpacity(self, cue):
		for i,t in enumerate(cue['tracks']):
			t["opacity"] = Launcher.op('ctrl_panels/track{}/opacity/out1'.format(i))['cross'].eval()
		return cue
	def WriteSpeed(self, cue):
		for i,t in enumerate(cue['tracks']):
			if i == 0:
				continue
			t["speed"] = Launcher.op('ctrl_panels/track{}/speed/out1'.format(i))['cross'].eval()
		return cue
	def WriteOperand(self, cue):
		cue["operand"] = Launcher.op('store').fetch('compOperand')
		return cue
	def WriteVolume(self, cue):
		for i,t in enumerate(cue['tracks']):
			if i == 0:
				continue
			t["volume"] = Launcher.op('ctrl_panels/track{}/volume/out1'.format(i))['cross'].eval()
		return cue
	def WriteBlind(self, cue):
		for i,t in enumerate(cue['tracks']):
			t["blind"] = Launcher.op('ctrl_panels/track{}/toggles/blind/out1'.format(i))['v1'].eval()
		return cue
	def WriteMute(self, cue):
		for i,t in enumerate(cue['tracks']):
			if i == 0:
				continue
			t["mute"] = Launcher.op('ctrl_panels/track{}/toggles/mute/out1'.format(i))['v1'].eval()
		return cue
	def WriteLoop(self, cue):
		for i,t in enumerate(cue['tracks']):
			if i == 0:
				continue
			t["loop"] = Launcher.op('ctrl_panels/track{}/toggles/loop/out1'.format(i))['v1'].eval()
		return cue
	def WriteFx(self, cue):
		for i,t in enumerate(cue['tracks']):
			base = []
			chain = Launcher.op('bus{}'.format(i)).FxChain()
			for f in chain:
				base.append({'id': f.name, 'settings': f.Save()})
			t["plugins"] = base
		return cue
	def WriteCue(self, scene, cid):
		cue = scene["cues"][cid]
		self.WriteSource(cue)
		self.WriteOpacity(cue)
		self.WriteOperand(cue)
		self.WriteVolume(cue)
		self.WriteSpeed(cue)
		self.WriteBlind(cue)
		self.WriteMute(cue)
		self.WriteLoop(cue)
		self.WriteFx(cue)
		scene["cues"][cid] = cue
		op(ipar.Set).SaveScene(scene)
		return
	def NewScene(self, sid):
		scene = op(ipar.Console).op('Factory').Scene(sid)
		op(ipar.Set).SaveScene(scene)
		run('op(ipar.Set).LoadScene("{}")'.format(sid), delayFrames = 1)
		return