import sys
mypath = project.folder + "/site-packages"
if mypath not in sys.path:
    sys.path.append(mypath)

import time
import dill as pickle
import json

ScaleRange = mod.Helpers.ScaleRange

Factory = op(ipar.Console).op('./Factory')
Set = op(ipar.Set)

store = op('store')

sourceMap = op('SourceMap')
blindMap = op('BlindMap')
muteMap = op('MuteMap')
loopMap = op('LoopMap')
operandMap = op('OperandMap')
opacityMap = op('OpacityMap')
volumeMap = op('VolumeMap')
speedMap = op('SpeedMap')
ctrl_panels = ops('ctrl_panels/track*')
buses = ops('bus[1-4]')
browser = op('browser')

volumeSliders = ops('ctrl_panels/track*/volume')
speedSliders = ops('ctrl_panels/track*/speed')

history = op('history')

buses.append(op('bus0'))

class LiveLauncher:
	def __init__(self, owner):
		self.o = owner
		return
	def SetSource(self, idx, src):
		buses[idx-1].par.Source = src
		store.store('trackSrc'+str(idx), src)
		return
	def SetOpacities(self, cueIdx):
		for t in ctrl_panels:
			sel = 't{}'.format(t.digits)
			v = opacityMap[cueIdx,sel]
			t.op('opacity').panel.u.val = v
		return
	def SetCtrl(self, cueIdx):
		for t in ctrl_panels:
			sel = "t{}".format(t.digits)
			t.op('toggles/blind').panel.state.val = op("BlindMap")[cueIdx, sel]
			if (t.digits == 0): #if master, dip now
				continue
			t.op('toggles/mute').panel.state.val = op("MuteMap")[cueIdx, sel]
			t.op('toggles/loop').panel.state.val = op("LoopMap")[cueIdx, sel]
		return
	def SetFx(self, cueIdx):
		# have to offset - 1... TODO: please standardize
		for i,t in enumerate(self.o.fetch('scene_viewing')["cues"][cueIdx - 1]["tracks"]):
			bus = self.o.op('bus{}'.format(i))
			bus.FillFx(t["plugins"])
	def SetOperand(self, cueIdx):
		store.store('compOperand', operandMap[cueIdx, 0].val)
		return
	def SetVolumes(self, cueIdx):
		for s in volumeSliders:
			tid = s.parent().digits
			sel = 't{}'.format(tid)
			v = volumeMap[cueIdx,sel]
			default = 1 if tid == 0 else 0
			s.panel.u.val = v or default
		return
	def SetSpeeds(self, cueIdx):
		for s in speedSliders:
			tid = s.parent().digits
			sel = 't{}'.format(tid)
			v = speedMap[cueIdx,sel]
			default = 1 if tid == 0 else 0
			s.panel.u.val = (v and ScaleRange(v,0,3,0,1)) or default
		return
	def SetCue(self, idx):
#		print("BEGIN SWITCH FRAME:", absTime.frame) 
		if self.o.fetch('scene_viewing')["id"] != self.o.fetch('scene_active')["id"]:
			self.o.store('scene_active', op(ipar.Set).fetch(self.o.fetch('scene_viewing')["id"]))
		store.store('cue', idx)
		if idx <= 2:
			store.store('pageStart', 1)
		else:
			store.store('pageStart', idx - 2)
		self.SetOpacities(idx)
		self.SetOperand(idx)
		self.SetVolumes(idx)
		self.SetSpeeds(idx)
		self.SetCtrl(idx)
		for c in browser.ops('cue{}/cell*'.format(idx)):
			self.SetSource(c.digits, str(c.op('bg').par.file))
		self.SetFx(idx)
#		print("END SWITCH FRAME:", absTime.frame)
		return
	def AddCue(self, idx):
		# have to offset - 1... TODO: please standardize
		print("add cue at idx {}".format(idx - 1))
		scene = json.loads(json.dumps(self.o.fetch('scene_viewing')))
		new = Factory.Cue(numTracks=ext.Helpers.CalcNumTracks() - 1) # offset tracks for master holy shi*t
		scene["cues"].insert(idx - 1, new)
		self.o.store('scene_viewing', scene)
		Set.SaveScene(scene)
		if idx <= op('store').fetch('cue'):
			op('store').store('cue', idx + 1)
		self.HardRefresh()
		return
	def DeleteCue(self, idx):
		# have to offset - 1... TODO: please standardize
		# BUG?: Should store cue idx as None if current scene deleted? Otherwise save before next launch will yield buggy behavior
		print("delete cue at idx {}".format(idx - 1))
		scene = json.loads(json.dumps(self.o.fetch('scene_viewing')))
		scene["cues"].pop(idx - 1)
		self.o.store('scene_viewing', scene)
		Set.SaveScene(scene)
		self.HardRefresh()
		return
	def StageTrackFx(self, trackIdx):
		for t in ctrl_panels:
			e = t.op('toggles/fx')
			if (e.panel.state == 1 and t.digits != trackIdx):
				e.panel.state = 1
		return
	def HardRefresh(self):
		sidActive = self.o.fetch("scene_active")["id"]
		sidViewing = self.o.fetch("scene_viewing")["id"]
		if (sidActive == sidViewing):
			self.o.store("scene_viewing", Set.fetch(sidViewing))
		self.o.store("scene_active", Set.fetch(sidActive)) 
		return
	def HandleSceneRename(self, prev, to):
		active = self.o.fetch("scene_active")["id"]
		viewing = self.o.fetch("scene_viewing")["id"]
		scene = Set.fetch(to)
		if prev == self.o.fetch("scene_active")["id"]:
			print("updating active")
			self.o.store("scene_active", Set.fetch(to))
		if prev == self.o.fetch("scene_viewing")["id"]:
			print("updating viewing")
			self.o.store("scene_viewing", Set.fetch(to))
		return
	def SyncToSet(self):
		self.o.store("scene_active", Set.fetch(set.par.Current.val))
		self.o.store("scene_viewing", Set.fetch(set.par.Current.val))
		return
	def DropFileInCell(self, cueIdx, trackNo, path):
		# have to offset - 1... TODO: please standardize
		print("drop file in cue {} track {}".format(cueIdx - 1, trackNo))
		scene = json.loads(json.dumps(self.o.fetch('scene_viewing')))
		track = scene['cues'][cueIdx - 1]['tracks'][trackNo]
		track['type'] = 'file'
		track['source'] = path
		self.o.store('scene_viewing', scene)
		Set.SaveScene(scene)
		Set.LoadScene(scene['id'])
		self.HardRefresh()
		return
	def DropTopInCell(self, cueIdx, trackNo, path):
		# have to offset - 1... TODO: please standardize
		print("drop TOP in cue {} track {}".format(cueIdx - 1, trackNo))
		scene = json.loads(json.dumps(self.o.fetch('scene_viewing')))
		track = scene['cues'][cueIdx - 1]['tracks'][trackNo]
		prevPath = track['source']
		track['type'] = 'file'
		track['source'] = path

		self.o.store('scene_viewing', scene)
		Set.SaveScene(scene)
		Set.LoadScene(scene['id'])
		self.HardRefresh()

		self.SetHistoryAction(
			'UNDO',
			lambda: self.DropTopInCell(cueIdx, trackNo, prevPath), # SAME cueIdx as OG PASSED
			'cue {}, Cell: {}: {}'.format(cueIdx, trackNo, path)
		)
		return
	def SetHistoryAction(self, key, action, label):
		history.store(key, {'action': pickle.dumps(action), 'label': label})
		return
	def LoadHistoryAction(self, key):
		b = history.fetch(key, None)
		if b:
			action = b['action']
			return pickle.loads(action)
