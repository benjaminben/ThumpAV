def onHoverStartGetAccept(comp, info):
	accepted = ['PLUGIN', 'PLUGIN_GROUP']
	try:
		if info['dragItems'][0] in accepted:
			return True
		else:
			return False
	except:
		return False

def onDropGetResults(comp, info):
	dragItems = info['dragItems']
	# expects sorted plugins
	plugins = dragItems[1]
	for p in plugins:
		if p:
			op(parent().par.Bus).SpawnFx(p)
	return {'comp': comp, 'received':dragItems}
