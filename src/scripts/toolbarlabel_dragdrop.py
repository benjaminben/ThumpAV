# callbacks for when associated Panel is being dropped on

def onHoverStartGetAccept(comp, info):
	### TEMP: 2025 DRAG/DROP BUG WORKAROUND ###
	if not len(info['dragItems']):
		return False
	valid = False
	label = info['dragItems'][1]
	if (label and type(label) == str and
    (label == 'PLUGIN' or label == 'PLUGIN_GROUP')):
		valid = True
	return valid # accept what is being dragged
	###########################################

	if not len(info['dragItems']):
		return False
	valid = False
	label = info['dragItems'][0]
	if (label and type(label) == str and
    (label == 'PLUGIN' or label == 'PLUGIN_GROUP')):
		valid = True
	return valid # accept what is being dragged
	
def onHoverEnd(comp, info):
	#debug('\nonHoverEnd comp:', comp.path, '- info:\n', info)

def onDropGetResults(comp, info):
	### TEMP: 2025 DRAG/DROP BUG WORKAROUND ###
	action = info['dragItems'][1]
	payload = info['dragItems'][2]
	chain = comp.parent.Bus.fetch("fx_chain", None)
	if (chain):
		myIdx = chain.index(comp.parent.Wrapper)
		if action == 'PLUGIN':
			srcComp = payload
			if srcComp.parent.Bus == comp.parent.Bus:
				draggedIdx = chain.index(srcComp)
				comp.parent.Bus.ReorderFx(draggedIdx, myIdx)
			else:
				comp.parent.Bus.SpawnFx(srcComp, myIdx)
		elif action == 'PLUGIN_GROUP':
			plugins = payload
			for p in plugins:
				if p.parent.Bus == comp.parent.Bus:
					destIdx = chain.index(comp.parent.Wrapper)
					draggedIdx = chain.index(p)
					comp.parent.Bus.ReorderFx(draggedIdx, destIdx)
				else:
					comp.parent.Bus.SpawnFx(p, myIdx)
	op.LiveLauncher.par.Showfxcopyarea = False
	return {'droppedOn': comp}
	###########################################

	action = info['dragItems'][0]
	payload = info['dragItems'][1]
	chain = comp.parent.Bus.fetch("fx_chain", None)
	if (chain):
		myIdx = chain.index(comp.parent.Wrapper)
		if action == 'PLUGIN':
			srcComp = payload
			if srcComp.parent.Bus == comp.parent.Bus:
				draggedIdx = chain.index(srcComp)
				comp.parent.Bus.ReorderFx(draggedIdx, myIdx)
			else:
				comp.parent.Bus.SpawnFx(srcComp, myIdx)
		elif action == 'PLUGIN_GROUP':
			plugins = payload
			for p in plugins:
				if p.parent.Bus == comp.parent.Bus:
					destIdx = chain.index(comp.parent.Wrapper)
					draggedIdx = chain.index(p)
					comp.parent.Bus.ReorderFx(draggedIdx, destIdx)
				else:
					comp.parent.Bus.SpawnFx(p, myIdx)
	op.LiveLauncher.par.Showfxcopyarea = False
	return {'droppedOn': comp}

# callbacks for when associated Panel is being dragged

def onDragStartGetItems(comp, info):
	### TEMP: 2025 DRAG/DROP BUG WORKAROUND ###
	staged = comp.parent.Bus.SelectStage
	sequence = sorted(staged, key=lambda item: staged[item]) # source index is key's value
	plugins = [None] * len(sequence)
	for idx, path in enumerate(sequence):
		plugins[idx] = op(path)
	dragItems = [comp, 'PLUGIN_GROUP', plugins]
	#debug('\nonDragStartGetItems comp:', comp.path, '- info:\n', info)
	op(ipar.LiveLauncher).par.Showfxcopyarea = True
	return dragItems
	###########################################

	staged = comp.parent.Bus.SelectStage
	sequence = sorted(staged, key=lambda item: staged[item]) # source index is key's value
	plugins = [None] * len(sequence)
	for idx, path in enumerate(sequence):
		plugins[idx] = op(path)
	dragItems = ['PLUGIN_GROUP', plugins]
	#debug('\nonDragStartGetItems comp:', comp.path, '- info:\n', info)
	op(ipar.LiveLauncher).par.Showfxcopyarea = True
	return dragItems

def onDragEnd(comp, info):
	#debug('\nonDragEnd comp:', comp.path, '- info:\n', info)
	
