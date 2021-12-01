class Factory():
	def __init__(self, owner):
		return
	def Cue(self, numTracks):
		cue = {
			'tracks': []
		}
		cue['tracks'].append(self.MasterTrack())
		for i in range(numTracks):
			cue['tracks'].append(self.Track())
		return cue
	def MasterTrack(self, options={}):
		default = {'blind': 0, 'opacity': 1.0, 'type': 'master', 'plugins': []}
		track = default
		for key in options:
			track[key] = options[key]
		return track
	def Track(self, options={}):
		default = {'mute': 1, 'operand': '', 'loop': 1, 'blind': 0, 'opacity': 1.0, 'volume': 1.0, 'speed': 1.0, 'type': None, 'source': '', 'plugins': [] }
		track = default
		for key in options:
			track[key] = options[key]
		return track
	def Scene(self, sid, numTracks=4, empty=False):
		scene = {'id': sid, 'cues': [] if empty else [self.Cue(numTracks)]}
		return scene