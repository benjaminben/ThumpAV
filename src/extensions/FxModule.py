class Plugin:
	def __init__(self, owner):
		self.owner = owner
		return
	def Load(self, options):
		# Caller requires but that's it
		return
	def Save(self) -> dict:
		# Caller consumes dict of settings
		options = {}
		return options