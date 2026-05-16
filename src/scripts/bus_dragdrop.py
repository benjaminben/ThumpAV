# callbacks for when associated Panel is being dropped on

def onHoverStartGetAccept(comp, info):
	"""
	Called when comp needs to know if dragItems are acceptable as a drop.

	Args:
		comp: the panel component being hovered over
		info: A dictionary containing all info about hover, including:
			dragItems: a list of objects being dragged over comp
			callbackPanel: the panel Component pointing to this callback DAT

	Returns:
		True if comp can receive dragItems
	"""
	return True

def onHoverEnd(comp, info):
	return

def onDropGetResults(comp, info):
	try:
		for item in info["dragItems"]:
			if type(item) == tdu.FileInfo:
				mfin = comp.SpawnFx("/main/console/fx_bin/selector_mfinTOP/Wrapper")
				mfin.par.Bypass = False
				mfin.op('Effect').par.File = item
	except Exception as ex:
		debug("Error dropping onto bus:", ex)
	return {'droppedOn': comp}

# callbacks for when associated Panel is being dragged

def onDragStartGetItems(comp, info):
	return

def onDragEnd(comp, info):
	return
	
