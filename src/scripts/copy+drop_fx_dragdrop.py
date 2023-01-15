def onHoverStartGetAccept(comp, info):
	accepted = ['PLUGIN', 'PLUGIN_GROUP', 'PLUGIN_PRESET']
	try:
		if info['dragItems'][0] in accepted:
			return True
		else:
			return False
	except:
		return False

def onDropGetResults(comp, info):
	print("HELLO", comp, info)
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
