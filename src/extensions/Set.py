TDF = op.TDModules.mod.TDFunctions

import json
sourceMap = op("source/map")

class Set:
	def __init__(self, owner):
		self.owner = owner
		TDF.createProperty(self, "Scenes", value={}, readOnly=False, dependable="deep")
		self.Scenes['__EMPTY__'] = op(ipar.Console).op('Factory').Scene('__EMPTY__')
		self.LoadAll()
		self.TOC = self.owner.op('toc')
		return
	def LoadAll(self):
		for ri in range(sourceMap.numRows):
			if ri == 0:
				continue
			self.LoadScene(sourceMap.cell(ri, "name").val)
	def LoadScene(self, scene):
		print("LOADING SCENE:", scene)
		s = None
		path = sourceMap.cell(scene, "path").val
		with open(path) as file:
			s = json.load(file)
		# if (s['id'] != scene): # force scene id to sync with filename 
		# 	print('Reassigning scene ID for', scene)
		# 	s['id'] = scene
		# 	with open(path, "w") as outfile:
		# 		json.dump(s, outfile)
		self.Scenes.val[scene] = s
		self.owner.store(scene, s)
	def Unload(self, scene):
		self.owner.unstore(scene)
	def UnloadAll(self):
		self.owner.unstore('*')
	def ReloadAll(self):
		self.UnloadAll()
		self.LoadAll()
	def SaveScene(self, scene, path=None): # update attribute and file
		print("SAVED SCENE:", scene["id"])
		sid = scene["id"]
		self.Scenes.val[scene["id"]] = scene
		
		dest = path or self.TOC[sid, 'path'].val

		print(dest, scene)

		with open(dest, "w") as outfile:
		# with open("{}/{}.json".format(sourceDir, sid), "w") as outfile:
			json.dump(scene, outfile)