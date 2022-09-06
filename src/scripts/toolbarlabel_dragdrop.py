# callbacks for when associated Panel is being dropped on

def onHoverStartGetAccept(comp, info):
	if not len(info['dragItems']):
		return False
	valid = False
	label = info['dragItems'][0]
	if (label and type(label) == str and
    (label == 'PLUGIN' or label == 'PLUGIN_GROUP')):
		valid = True
	return valid # accept what is being dragged
	
def onHoverEnd(comp, info):
	"""
	Called when dragItems leave comp's hover area.

	Args:
		comp: the panel component being hovered over
		info: A dictionary containing all info about hover, including:
			dragItems: a list of objects being dragged over comp
			callbackPanel: the panel Component pointing to this callback DAT
	"""
	#debug('\nonHoverEnd comp:', comp.path, '- info:\n', info)

def onDropGetResults(comp, info):
	"""
	Called when comp receives a drop of dragItems. This will only be called if
	onHoverStartGetAccept has returned True for these dragItems.

	Args:
		comp: the panel component being dropped on
		info: A dictionary containing all info about drop, including:
			dragItems: a list of objects being dropped on comp
			callbackPanel: the panel Component pointing to this callback DAT

	Returns:
		 dictionary of results with descriptive keys. Some possibilities:
			'droppedOn': the object receiving the drop
			'createdOPs': list of created ops in order of drag items
			'dropChoice': drop menu choice selected
			'modified': object modified by drop
	"""
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
	op(ipar.LiveLauncher).par.Showfxcopyarea = False
	return {'droppedOn': comp}

# callbacks for when associated Panel is being dragged

def onDragStartGetItems(comp, info):
	"""
	Called when information about dragged items is required.

	Args:
		comp: the panel clicked on to start drag
		info: A dictionary containing all info about drag
			callbackPanel: the panel Component pointing to this callback DAT

	Returns:
		A list of dragItems: [object1, object2, ...]
	"""
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
	"""
	Called when a drag action ends.

	Args:
		comp: the panel clicked on to start drag
		info: A dictionary containing all info about drag, including:
			accepted: True if the drag was accepted, False if not
			dropResults: a dict of drop results. This is the return value of 
				onDropGetResults
			dragItems: the original dragItems for the drag
			callbackPanel: the panel Component pointing to this callback DAT
	"""
	#debug('\nonDragEnd comp:', comp.path, '- info:\n', info)
	
