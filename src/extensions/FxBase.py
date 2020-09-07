class FxBase:
	def __init__(self, owner):
		return
	def loadParameter(self, param, val):
		if type(val) == str:
			param.expr = val
		else:
			param.val = val
	def saveParameter(self, param):
		val = None
		if param.mode == ParMode.EXPRESSION:
			val = param.expr
		else:
			val = param.eval()
		return val
