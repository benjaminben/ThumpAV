class Main:
	def __init__(self, ownerComp):
		self.owner = ownerComp
		return
	def SyncMonitors(self):
		monitorsDat = self.owner.op('monitors')
		uiWidth = self.owner.par.Uiresx
		uiHeight = self.owner.par.Uiresy
		mainWidth = uiWidth
		mainHeight = uiHeight
		for i in range(1, monitorsDat.numRows):
			monWidth = int(monitorsDat[i, 'width'].val or 0)
			monHeight = int(monitorsDat[i, 'height'].val)
			mon = self.owner.op('monitor'+str(i))
			mon.par.w = monWidth
			mon.par.h = monHeight
			mainWidth += monWidth			
			if monHeight > mainHeight:
				mainHeight = monHeight
		self.owner.par.w = mainWidth
		self.owner.par.h = mainHeight
	def RebaseBank(self):
		return