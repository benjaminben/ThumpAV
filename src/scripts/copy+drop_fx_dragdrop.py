def onHoverStartGetAccept(comp, info):
	accepted = ['PLUGIN', 'PLUGIN_GROUP', 'PLUGIN_PRESET']
	### TEMP: 2025 DRAG/DROP BUG WORKAROUND ###
	try:
		if info['dragItems'][1] in accepted:
			return True
		else:
			return False
	except:
		return False
	###########################################
	try:
		if info['dragItems'][0] in accepted:
			return True
		else:
			return False
	except:
		return False

def onDropGetResults(comp, info):
	### TEMP: 2025 DRAG/DROP BUG WORKAROUND ###
	bus = op(comp.parent().par.Bus)
	dragItems = info['dragItems']
	if dragItems[1] == 'PLUGIN_PRESET':
		bus.LoadPreset(dragItems[2])
	else:
		# expects sorted plugins
		plugins = dragItems[2]
		for p in plugins:
			if p:
				bus.SpawnFx(p)
	return {'comp': comp, 'received':dragItems}
	###########################################
	bus = op(comp.parent().par.Bus)
	dragItems = info['dragItems']
	if dragItems[0] == 'PLUGIN_PRESET':
		bus.LoadPreset(dragItems[1])
	else:
		# expects sorted plugins
		plugins = dragItems[1]
		for p in plugins:
			if p:
				bus.SpawnFx(p)
	return {'comp': comp, 'received':dragItems}
