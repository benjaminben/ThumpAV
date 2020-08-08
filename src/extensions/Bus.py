fxBin = op(ipar.Console).op('fx_bin')

class BusClass:
	def __init__(self, owner):
		self.o = owner
	def Boop(self, s):
		print(s)
	def FxChain(self):
		return self.o.fetch('fx_chain', [])
	def FillFx(self, chain):
		fxChain = self.FxChain()[:]
		ptChain = chain[:]
		nuChain = []
		reroute = len(fxChain) != len(ptChain)
		if self.o.op('override').panel.state.val:
			return
		while len(ptChain):
			node = False
			for i,f in enumerate(fxChain):
				if f.name == ptChain[0]["id"]:
					node = fxChain.pop(i)
					if i: # confirm if we've gone farther than 0 (recycle f but new order)
						reroute = True
					break
			popd = ptChain.pop(0)
			if not node:
				#print('creating', popd['id'])
				node = self.o.copy(fxBin.op('{name}/{name}'.format(name=popd['id'])))
				node.par.display = True
				reroute = True
			node.Load(chain[len(nuChain)]['settings'])
			nuChain.append(node)
		if len(fxChain):
			while len(fxChain):
				f = fxChain.pop(len(fxChain) - 1)
				print('destroy', f.name)
				f.destroy()
		if reroute:
			print('rerouting')
			self.o.store('fx_chain', nuChain)
			self.RouteFx()
		return
	def KillFx(self, fx):
		idx = 0
		a = self.FxChain()
		for f in a:
			if f == fx:
				a.pop(idx)
				break
			idx += 1
		self.o.store('fx_chain', a)
		fx.destroy()
		self.RouteFx()
	def SpawnFx(self, path):
		fxArr = self.FxChain()
		for f in fxArr:
			if (op(path).name == f.name):
				return
		newFx = self.o.copy(op(path))
		newFx.par.display = True
		fxArr.append(newFx)
		self.o.store('fx_chain', fxArr)
		self.RouteFx()
	def RouteFx(self):
		i = 0
		fx_chain = self.FxChain()

		if not len(fx_chain):
			self.o.op('preFx').outputConnectors[0].connect(self.o.op('postFx'))

		while i < len(fx_chain):
			fx_chain[i].par.alignorder = i
			if (i == 0):
				self.o.op('preFx').outputConnectors[0].connect(fx_chain[i].inputConnectors[0])
			else:
				fx_chain[i-1].outputConnectors[0].connect(fx_chain[i].inputConnectors[0])
				# print('connected', fx_chain[i-1], 'to', fx_chain[i])
			i += 1
			if (i == len(fx_chain)):
				fx_chain[i-1].outputConnectors[0].connect(self.o.op('postFx'))
	def ReorderFx(self, oId, nId):
		chain = self.FxChain()
		chain.insert(nId, chain.pop(oId))
		self.o.store('fx_chain', chain)
		self.RouteFx()