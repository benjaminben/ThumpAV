Set = op(ipar.Set)
Factory = op(ipar.Console).op('./Factory')

class Browser:
	def __init__(self, owner):
		self.owner = owner
		# self.ActiveScene = owner.par.Scene.eval()
		# self.ViewingScene = owner.par.Scene.eval()
		return
	def PageNext(self):
		cues = self.owner.par.Data.eval()['cues']
		pageTo = self.owner.par.Pagestart + self.owner.par.Perpage
		if (pageTo > len(cues) - 1 + self.owner.par.Perpage):
			pageTo = len(cues) - self.owner.par.Perpage
		self.owner.par.Pagestart = pageTo
		return
	def PagePrev(self):
		pageTo = self.owner.par.Pagestart - self.owner.par.Perpage
		if (pageTo < 1):
			pageTo = 1
		self.owner.par.Pagestart = pageTo
		return
	def NextCue(self):
		cues = self.owner.par.Data.eval()["cues"]
		if self.owner.par.Latestcue == len(cues) - 1:
			return
		destIdx = self.owner.par.Latestcue + 1
		self.SendCue(cues[destIdx], destIdx)
	def PrevCue(self):
		cues = self.owner.par.Data.eval()["cues"]
		if self.owner.par.Latestcue == 0:
			return
		destIdx = self.owner.par.Latestcue - 1
		self.SendCue(cues[destIdx], destIdx)
	def SendCue(self, cue, idx):
		if idx <= 2:
			self.owner.par.Pagestart = 1
		else:
			self.owner.par.Pagestart = idx - 1
		self.owner.parent.LiveLauncher.SetCue(cue, self.owner)
		self.owner.par.Latestcue = idx
	def AddCue(self, idx):
		# have to offset - 1... TODO: please standardize
		print("add cue at idx {}".format(idx - 1))
		sceneData = self.owner.par.Data.eval()
		new = Factory.Cue(numTracks=self.CalcNumTracks() - 1) # offset tracks for master holy shi*t
		scene = sceneData.getRaw()
		scene["cues"].insert(idx - 1, new)
		#self.o.store('scene_viewing', scene)
		Set.SaveScene(scene)
		if idx <= self.owner.par.Latestcue:
			self.owner.par.Latestcue = idx + 1
		#self.HardRefresh()
		return
	def DeleteCue(self, idx):
		# have to offset - 1... TODO: please standardize
		# BUG?: Should store cue idx as None if current scene deleted? Otherwise save before next launch will yield buggy behavior
		print("delete cue at idx {}".format(idx - 1))
		scene = self.owner.par.Data.eval().getRaw()
		scene["cues"].pop(idx - 1)
		Set.SaveScene(scene)
		#self.HardRefresh()
		return
	def DropCellInCell(self, cueIdx, trackNo, ref):
		return
	def DropFileInCell(self, cueIdx, trackNo, path):
		# have to offset - 1... TODO: please standardize
		print("FILE DROP??", path)
		print("drop file in cue {} track {}".format(cueIdx - 1, trackNo))
		scene = self.owner.par.Data.eval().getRaw()
		track = scene['cues'][cueIdx - 1]['tracks'][trackNo]
		track['type'] = 'file'
		track['source'] = path
		
		Set.SaveScene(scene)
		return
	def DropTopInCell(self, cueIdx, trackNo, path):
		# have to offset - 1... TODO: please standardize
		print("drop TOP in cue {} track {}".format(cueIdx - 1, trackNo))
		scene = self.owner.par.Data.eval().getRaw()
		track = scene['cues'][cueIdx - 1]['tracks'][trackNo]
		prevPath = track['source']
		track['type'] = 'file'
		track['source'] = path

		Set.SaveScene(scene)

		ext.LiveLauncher.SetHistoryAction(
			'UNDO',
			lambda: self.DropTopInCell(cueIdx, trackNo, prevPath), # SAME cueIdx as OG PASSED
			'cue {}, Cell: {}: {}'.format(cueIdx, trackNo, path)
		)
		return
	def HandleSceneRename(self, prev, to):
		active = self.SceneActive
		viewing = Set.par.Current.eval()
		scene = Set.Scenes.val[to]
		if prev == self.SceneActive:
			print("updating active")
			self.SceneActive = to
		return
	def CalcNumTracks(self):
		numTracks = 0
		for cue in self.owner.par.Data.eval()["cues"]:
			if len(cue["tracks"]) > numTracks:
				numTracks = len(cue["tracks"])
		return numTracks
	def SaveCue(self):
		cid = self.owner.par.Latestcue.eval()
		scene = op(ipar.Set).Scenes.val[self.owner.par.Scene.eval()].getRaw()
		op(ipar.Writer).WriteCue(scene, cid)