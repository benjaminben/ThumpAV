
def loadConstant(param, val):
	param.val = val

def loadExpression(param, val):
	param.expr = val

def loadBind(param, val):
	param.bindExpr = val

def saveConstant(param):
	return {
		'mode': 'CONSTANT',
		'd': param.eval() }

def saveExpression(param):
	return {
		'mode': 'EXPRESSION',
		'd': param.expr }

def saveBind(param):
	return {
		'mode': 'BIND',
		'd': param.bindExpr }

def saveExport(param):
	print('Constant val substituted for export when saving:', param)
	return {
		'mode': 'CONSTANT', # NO SAVING EXPORTS yet?
		'd': param.eval() }

loadSwitcher = {
	'CONSTANT': loadConstant,
	'EXPRESSION': loadExpression,
	'BIND': loadBind,
}

saveSwitcher = {
	'CONSTANT': saveConstant,
	'EXPRESSION': saveExpression,
	'BIND': saveBind,
	'EXPORT': saveExport,
}

def loadParameter(param, src):
	# Load attaches a value to a parameter without returning anything
	mode = None
	loaderFunc = None
	
	try:
		mode = src['mode']
	except NameError:
		mode = 'CONSTANT'
	except TypeError:
		param = src
		return
	
	try:
		loaderFunc = loadSwitcher[mode]
	except NameError as ex:
		print(ex)
		loaderFunc = loadConstant
	loaderFunc(param, src['d'])

def saveParameter(param):
	# Save returns a value to be written to JSON
	saveFunc = saveSwitcher[param.mode.name]
	return saveFunc(param)


class FxBase:
	def __init__(self, owner):
		return
	def loadParameter(self, param, src):
		# Load attaches a value to a parameter without returning anything
		mode = None
		loaderFunc = None
		
		try:
			mode = src['mode']
		except NameError:
			mode = 'CONSTANT'
		except TypeError:
			param = src
			return
		
		try:
			loaderFunc = loadSwitcher[mode]
		except NameError:
			loaderFunc = loadConstant
		loaderFunc(param, src['d'])
	def saveParameter(self, param):
		# Save returns a value to be written to JSON
		saveFunc = saveSwitcher[param.mode.name]
		return saveFunc(param)
