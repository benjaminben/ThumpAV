import json
import traceback
import random

Plugin = mod("/main/console/fx_bin/PluginBase").Plugin
fxHelp = mod("/main/console/fx_bin/FxBase")\

default = {
}

class Effect(Plugin):
	def __init__(self, owner):
		super(Effect, self).__init__(owner)
		self.CueList = []
		self.bus = self.owner.parent.Bus
		self.LatestIdx = 0
		return
	def Reset(self):
		self.Load(default)
	def Load(self, options):
		super(Effect, self).Load(options)
		for page in self.owner.customPages:
			for p in page.pars:
				if p.name in options.get('Effect', {}):
					p.val = options['Effect'][p.name]
					#fxHelp.loadParameter(p, options['Effect'][p.name])
		return
	def Save(self):
		settings = super(Effect, self).Save()
		settings['Effect'] = {}
		for page in self.owner.customPages:
			for p in page.pars:
				settings['Effect'][p.name] = p.eval()
				#settings['Effect'][p.name] = fxHelp.saveParameter(p)
		return settings
	def SaveBusStateToCue(self, idx = None):
		base = []
		chain = self.bus.FxChain()
		for f in chain:
			base.append({'id': f.par.Name.eval(), 'settings': f.Save()})
		cuelist = self.GetCuelist()
		print(self.owner, idx, cuelist)
		if isinstance(idx, int):
			cuelist[idx] = base
		else:
			cuelist.append(base)
			idx = len(cuelist) - 1
		self.owner.par.Cuelistjson = cuelist
		#self.owner.op('ctrl_list').selections = [(idx, 0, idx, 2)]
		self.LatestIdx = idx
		return cuelist
	def LaunchOnDeck(self):
		od = self.owner.par.Ondeck.eval() 
		self.LaunchCueByIdx(od)
		self.SetOnDeck(od)
	def LaunchCueByIdx(self, idx):
		cuelist = self.GetCuelist()
		self.bus.FillFx(cuelist[idx])
		self.LatestIdx = idx
	def DeleteIdx(self, idx = 0):
		cuelist = self.GetCuelist()
		cuelist.pop(idx)
		parent.Effect.par.Cuelistjson = cuelist
	def GetCuelist(self):
		cuelist = self.owner.par.Cuelistjson.eval()
		return cuelist if cuelist else []
		#return json.loads(self.owner.par.Cuelistjson.eval())
	def ResetCuelist(self):
		self.owner.par.Cuelistjson = [[]]
		self.owner.op('countStep').par.resetpulse.pulse()
	def SetOnDeck(self, prev = 0):
		mode = self.owner.par.Ondeckmode.eval()
		cuelist = self.GetCuelist()[:]
		idx = prev
		numcues = len(cuelist)
		if numcues > 1:
			if mode == "increment":
				idx += 1
				if idx > numcues - 1:
					idx = 0 
			elif mode == "random":
				l = list(range(0, len(cuelist)))
				l.pop(prev)
				idx = l[random.randint(0, len(l) - 1)]
			self.owner.par.Ondeck = idx