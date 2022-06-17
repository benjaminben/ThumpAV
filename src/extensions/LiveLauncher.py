import sys
mypath = project.folder + "/site-packages"
if mypath not in sys.path:
    sys.path.append(mypath)

import time
import dill as pickle
import json

import TDFunctions as TDF

ScaleRange = mod.Helpers.ScaleRange

store = op('store')

ctrl_panels = ops('ctrl_panels/track*')
buses = ops('bus[1-4]')
browser = op('browser')

volumeSliders = ops('ctrl_panels/track*/volume')
speedSliders = ops('ctrl_panels/track*/speed')

history = op('history')

buses.append(op('bus0'))

Playback = op('Playback')

class LiveLauncher:
	def __init__(self, owner):
		self.o = owner
		self.o.store("ActiveBrowser", Playback.ActiveBrowser())
		return
	def SetSource(self, idx, src):
		buses[idx-1].par.Source = src
		return
	def SetOpacities(self, cue):
		for t in ctrl_panels:
			sel = 't{}'.format(t.digits)
			v = cue['tracks'][t.digits]['opacity']
			t.op('opacity').par.Value0 = v
		return
	def SetCtrl(self, cue):
		for t in ctrl_panels:
			sel = "t{}".format(t.digits)
			t.op('toggles/blind').par.Value0 = bool(cue['tracks'][t.digits]['blind'])
			if (t.digits == 0): #if master, dip now
				continue
			t.op('toggles/mute').par.Value0 = cue['tracks'][t.digits]['mute']
			t.op('toggles/loop').par.Value0 = cue['tracks'][t.digits]['loop']
		return
	def SetFx(self, cue):
		# have to offset - 1... TODO: please standardize
		for i,t in enumerate(cue["tracks"]):
			bus = self.o.op('bus{}'.format(i))
			bus.FillFx(t["plugins"].getRaw())
	def SetOperand(self, cue):
		for t in ctrl_panels:
			if (t.digits == 0): #if master, dip now
				continue
			sel = "t{}".format(t.digits)
			bus = self.o.op(f'bus{t.digits}')
			bus.par.Operand = cue['tracks'][t.digits]['operand']
		return
	def SetVolumes(self, cue):
		for s in volumeSliders:
			tid = s.parent().digits
			sel = 't{}'.format(tid)
			v = cue['tracks'][tid]['volume']
			default = 1 if tid == 0 else 0
			s.par.Value0 = v or default
		return
	def SetSpeeds(self, cue):
		for s in speedSliders:
			tid = s.parent().digits
			sel = 't{}'.format(tid)
			v = cue['tracks'][tid]['speed']
			default = 1 if tid == 0 else 0
			s.par.value0 = v or default
		return
	def SetCue(self, cue, browser):
		tracks = cue['tracks']
#		print("BEGIN SWITCH FRAME:", absTime.frame)
		self.o.store("ActiveBrowser", browser)
		self.SetOpacities(cue)
		self.SetOperand(cue)
		self.SetVolumes(cue)
		self.SetSpeeds(cue)
		self.SetCtrl(cue)
		for cidx in range(1, len(tracks)):
			self.SetSource(cidx, tracks[cidx]['source'])
		self.SetFx(cue)
#		print("END SWITCH FRAME:", absTime.frame)
		return
	def SetLayer(self, trackIdx, data):
		self.SetSource(trackIdx, data['source'])
		bus = self.o.op('bus{}'.format(trackIdx))
		bus.FillFx(data['plugins'].getRaw())
		bus.par.Operand = data['operand']
		print(data, track)
		return
	def StageTrackFx(self, trackIdx):
		self.o.op(f'ctrl_panels/track{trackIdx}/toggles/fx').par.Value0 = 1
		return
	def SetHistoryAction(self, key, action, label):
		history.store(key, {'action': pickle.dumps(action), 'label': label})
		return
	def LoadHistoryAction(self, key):
		b = history.fetch(key, None)
		if b:
			action = b['action']
			return pickle.loads(action)
