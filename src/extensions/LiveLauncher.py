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
		self.SceneActive = op(ipar.Set).par.Current.eval()
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
		for i,t in enumerate(Set.Scenes.val[Set.par.Current.eval()]["cues"][cueIdx - 1]["tracks"]):
			bus = self.o.op('bus{}'.format(i))
			bus.FillFx(t["plugins"].getRaw())
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
		if Set.par.Current.eval() != self.SceneActive:
			self.SceneActive = op(ipar.Set).par.Current.eval()
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
		new = Factory.Cue(numTracks=ext.Helpers.CalcNumTracks() - 1) # offset tracks for master holy shi*t
		scene = Set.Scenes.val[Set.par.Current.eval()].getRaw()
		scene["cues"].insert(idx - 1, new)
		#self.o.store('scene_viewing', scene)
		Set.SaveScene(scene)
		if idx <= store.fetch('cue'):
			store.store('cue', idx + 1)
		#self.HardRefresh()
		return
	def DeleteCue(self, idx):
		# have to offset - 1... TODO: please standardize
		# BUG?: Should store cue idx as None if current scene deleted? Otherwise save before next launch will yield buggy behavior
		print("delete cue at idx {}".format(idx - 1))
		scene = Set.Scenes.val[Set.par.Current.eval()].getRaw()
		scene["cues"].pop(idx - 1)
		Set.SaveScene(scene)
		#self.HardRefresh()
		return
	def StageTrackFx(self, trackIdx):
		for t in ctrl_panels:
			e = t.op('toggles/fx')
			if (e.panel.state == 1 and t.digits != trackIdx):
				e.panel.state = 1
		return
	def HandleSceneRename(self, prev, to):
		active = self.SceneActive
		viewing = Set.par.Current.eval()
		scene = Set.Scenes.val[to]
		if prev == self.SceneActive:
			print("updating active")
			self.SceneActive = to
		return
	def DropFileInCell(self, cueIdx, trackNo, path):
		# have to offset - 1... TODO: please standardize
		print("drop file in cue {} track {}".format(cueIdx - 1, trackNo))
		scene = Set.Scenes.val[Set.par.Current.eval()].getRaw()
		track = scene['cues'][cueIdx - 1]['tracks'][trackNo]
		track['type'] = 'file'
		track['source'] = path
		#self.o.store('scene_viewing', scene)
		Set.SaveScene(scene)
		#Set.LoadScene(scene['id'])
		#self.HardRefresh()
		return
	def DropTopInCell(self, cueIdx, trackNo, path):
		# have to offset - 1... TODO: please standardize
		print("drop TOP in cue {} track {}".format(cueIdx - 1, trackNo))
		scene = Set.Scenes.val[Set.par.Current.eval()].getRaw()
		track = scene['cues'][cueIdx - 1]['tracks'][trackNo]
		prevPath = track['source']
		track['type'] = 'file'
		track['source'] = path

		#self.o.store('scene_viewing', scene)
		Set.SaveScene(scene)
		#Set.LoadScene(scene['id'])
		#self.HardRefresh()

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
